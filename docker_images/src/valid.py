import os
import time
import torch
import argparse
import scipy.io
import warnings
from torch.autograd import Variable
from torchvision import datasets, transforms

import datetime
import warnings
warnings.simplefilter("ignore", UserWarning)
warnings.simplefilter("ignore", RuntimeWarning)

import dataset
from darknet import Darknet
from utils import *
from MeshPly import MeshPly

def valid(datacfg, modelcfg, weightfile):
    def truths_length(truths, max_num_gt=50):
        for i in range(max_num_gt):
            if truths[i][1] == 0:
                return i
    # class_name 
    c_id = datacfg.split('/')[1]
    c_kor = id2kor(c_id)
    c_eng = id2eng(c_id)

    # Parse configuration files
    data_options = read_data_cfg(datacfg)
    valid_images = data_options['valid']
    meshname     = data_options['mesh']
    backupdir    = data_options['backup']
    name         = data_options['name']
    gpus         = data_options['gpus'] 
    im_width     = int(data_options['width'])
    im_height    = int(data_options['height'])
    if not os.path.exists(backupdir):
        makedirs(backupdir)

    # Parameters
    seed = int(time.time())
    os.environ['CUDA_VISIBLE_DEVICES'] = gpus
    torch.cuda.manual_seed(seed)
    save            = True
    proj            = True
    vis             = True
    num_classes     = 1
    testing_samples = 0.0

    # To save
    testing_error_pixel = 0.0
    iou_acc = []
    iou_convex_acc = []
    errs_2d = []
    errs_3d = []

    # Read object model information, get 3D bounding box corners
    mesh      = MeshPly(meshname)
    vertices = np.c_[np.array(mesh.vertices), np.ones((len(mesh.vertices), 1))].transpose()
    indices = np.c_[np.array(mesh.indices), np.ones((len(mesh.indices), 2))].transpose()
    corners3D = get_3D_corners(vertices)
    try:
        diam  = float(options['diam'])
    except:
        diam  = calc_pts_diameter(np.array(mesh.vertices))
        
    # Get validation file names
    with open(valid_images) as fp:
        tmp_files = fp.readlines()
        valid_files = [item.rstrip() for item in tmp_files]
    
    # Specicy model, load pretrained weights, pass to GPU and set the module in evaluation mode
    model = Darknet(modelcfg)
    model.print_network()
    model.load_weights(weightfile)
    model.cuda()
    model.eval()
    test_width    = model.test_width
    test_height   = model.test_height
    num_keypoints = model.num_keypoints
    num_labels    = num_keypoints * 2 + 3 # +2 for width, height,  +1 for class label

    # Get the parser for the test dataset
    valid_dataset = dataset.listDataset(valid_images,
                                        shape=(test_width, test_height),
                                        shuffle=False,
                                        transform=transforms.Compose([transforms.ToTensor(),]))

    # Specify the number of workers for multiple processing, get the dataloader for the test dataset
    kwargs = {'num_workers': 4, 'pin_memory': True}
    test_loader = torch.utils.data.DataLoader(valid_dataset, batch_size=1, shuffle=False, **kwargs)

    # Iterate through test batches (Batch size for test data is 1)
    count = 0

    # save experiment results as CSV format
    class_name = test_loader.dataset.lines[0].split('/')[-1].split('_')[0]

    if save:
        if (os.path.isdir("experimental_results") == 0): makedirs('experimental_results')
        c = open('experimental_results/'+class_name+'.csv', 'w', encoding="UTF-8")
        c.write('Data ID, x0-GT, y0-GT, x1-GT, y1-GT, x2-GT, y2-GT, x3-GT, y3-GT, x4-GT, y4-GT, x5-GT, y5-GT, x6-GT, y6-GT, x7-GT, y7-GT, x8-GT, y8-GT, x0-predict, y0-predict, x1-predict, y1-predict, x2-predict, y2-predict, x3-predict, y3-predict, x4-predict, y4-predict, x5-predict, y5-predict, x6-predict, y6-predict, x7-predict, y7-predict, x8-predict, y8-predict, pixel error, projection test, IoU score, IoU test, \n')

    for batch_idx, (data, target) in enumerate(test_loader):

        with open(test_loader.dataset.lines[batch_idx].replace('images', 'cams').replace('.png', '.txt').replace('\n', '')) as f:
            # Camera params.
            rdata = f.readlines()
            [fx, fy, u0, v0] = rdata[0].split(" ")
            [fx, fy, u0, v0] = [float(fx), float(fy), float(u0), float(v0)]
            intrinsic_calibration = get_camera_intrinsic(u0, v0, fx, fy)
            data_id = test_loader.dataset.lines[batch_idx].split('/')[-1][:-5]

        # Pass data to GPU
        data = data.cuda()
        target = target.cuda()

        # Wrap tensors in Variable class, set volatile=True for inference mode and to use minimal memory during inference
        data = Variable(data, volatile=True)

        # Forward pass
        output = model(data).data

        # Using confidence threshold, eliminate low-confidence predictions
        all_boxes = get_region_boxes(output, num_classes, num_keypoints)

        # Evaluation
        # Iterate through all batch elements
        for box_pr, target in zip([all_boxes], [target[0]]):

            # For each image, get all the targets (for multiple object pose estimation, there might be more than 1 target per image)
            truths = target.view(-1, num_labels)

            # Get how many objects are present in the scene
            num_gts    = truths_length(truths)

            # Iterate through each ground-truth object
            for k in range(num_gts):
                box_gt = list()
                for j in range(1, 2*num_keypoints+1):
                    box_gt.append(truths[k][j])
                box_gt.extend([1.0, 1.0])
                box_gt.append(truths[k][0])

                # Denormalize the corner predictions
                corners2D_gt = np.array(np.reshape(box_gt[:18], [-1, 2]), dtype='float32')
                corners2D_pr = np.array(np.reshape(box_pr[:18], [-1, 2]), dtype='float32')
                corners2D_gt[:, 0] = corners2D_gt[:, 0] * im_width
                corners2D_gt[:, 1] = corners2D_gt[:, 1] * im_height
                corners2D_pr[:, 0] = corners2D_pr[:, 0] * im_width
                corners2D_pr[:, 1] = corners2D_pr[:, 1] * im_height

                # write gt, predict
                gt = ''
                for i in range(9):
                    gt += '{:.1f},'.format(corners2D_gt[i][0])
                    gt += '{:.1f},'.format(corners2D_gt[i][1])
                predict = ''
                for i in range(9):
                    predict += '{:.1f},'.format(corners2D_pr[i][0])
                    predict += '{:.1f},'.format(corners2D_pr[i][1])

                # Compute [R|t] by pnp
                R_gt, t_gt = pnp(np.array(np.transpose(np.concatenate((np.zeros((3, 1)), corners3D[:3, :]), axis=1)), dtype='float32'),  corners2D_gt, np.array(intrinsic_calibration, dtype='float32'))
                R_pr, t_pr = pnp(np.array(np.transpose(np.concatenate((np.zeros((3, 1)), corners3D[:3, :]), axis=1)), dtype='float32'),  corners2D_pr, np.array(intrinsic_calibration, dtype='float32'))

                # Compute pixel error
                Rt_gt        = np.concatenate((R_gt, t_gt), axis=1)
                Rt_pr        = np.concatenate((R_pr, t_pr), axis=1)
                proj_2d_gt   = compute_projection(vertices, Rt_gt, intrinsic_calibration)
                proj_2d_pred = compute_projection(vertices, Rt_pr, intrinsic_calibration)
                norm         = np.linalg.norm(proj_2d_gt - proj_2d_pred, axis=0)
                pixel_dist   = np.mean(norm)
                errs_2d.append(pixel_dist)

                # Compute 3D distances
                transform_3d_gt   = compute_transformation(vertices, Rt_gt)
                transform_3d_pred = compute_transformation(vertices, Rt_pr)
                norm3d            = np.linalg.norm(transform_3d_gt - transform_3d_pred, axis=0)
                vertex_dist       = np.mean(norm3d)
                errs_3d.append(vertex_dist)

                # Projection
                frame = valid_files[count][-8:-4]

                if proj==True:
                    if(os.path.isdir("experimental_results")==0): makedirs('experimental_results')
                    if(os.path.isdir("experimental_results/" + name + "_result") == 0): os.mkdir("experimental_results/" + name + "_result")

                    np.savetxt("experimental_results/" + name + "_result" + "/corners_" + valid_files[count][-8:-3] + "txt", np.array(corners2D_pr, dtype='float32'))
                    np.savetxt("experimental_results/" + name + "_result" + "/R_" + valid_files[count][-8:-3] + "txt", np.array(R_pr, dtype='float32'))
                    np.savetxt("experimental_results/" + name + "_result" + "/t_" + valid_files[count][-8:-3] + "txt", np.array(t_pr, dtype='float32'))
                    K = np.array([[fx, 0, u0], [0, fy, v0], [0, 0, 1]])
                    R = np.loadtxt("experimental_results/" + name + "_result" + "/R_{}.txt".format(frame))
                    t = np.loadtxt("experimental_results/" + name + "_result" + "/t_{}.txt".format(frame))
                    RT = np.vstack([R.T, t]).T
                    f_prj = open("experimental_results/" + name + "_result" + "/prj_{}.txt".format(frame), 'w')
                    for i in range(vertices.shape[1]):
                        p_n = RT @ np.transpose(vertices[:,i])
                        p = K @ np.transpose([ p_n[0]/p_n[2], p_n[1]/p_n[2], 1 ])
                        p_x = int(p[0]/p[2]+0.5)
                        p_y = int(p[1]/p[2]+0.5)
                        f_prj.write("{} {}\n".format(p_x, p_y))
                    f_prj.close()

                    f_ind = open("experimental_results/" + name + "_result" + "/ind_{}.txt".format(frame), 'w')
                    for j in range(indices.shape[1]):
                        f_ind.write("{} {} {}\n".format(int(indices[0,j]), int(indices[1,j]), int(indices[2,j])))
                    f_ind.close()

                    ## Compute IoU
                    iou = compute_iou(name, frame, True)
                    iou_convex = compute_convexhull_iou(corners2D_gt, corners2D_pr)
                    print("[#{:04d}] {}: {:.2f} (pixel dist.), {:.2f} (IoU score)".format(count, frame, pixel_dist, iou_convex))
                else:
                    iou_convex = compute_convexhull_iou(corners2D_gt, corners2D_pr)
                    iou = iou_convex

                iou_acc.append(iou)
                iou_convex_acc.append(iou_convex)
                if vis:
                    visualize(name, frame, corners3D)

                # Sum errors
                testing_error_pixel  += pixel_dist
                testing_samples      += 1
                if save:
                    # csv write
                    context = data_id + ',' + gt + predict + '{:.2f}, {}, {:.2f}, {}\n'.format(pixel_dist,
                                                                                               pixel_dist <= 10, iou_convex,
                                                                                               iou_convex >= 0.5)
                    c.write(context)

                count = count + 1

    if save:
        c.close()

    # Compute 2D projection / IoU based Accuracy
    px_threshold = 10 # pixel threshold for 2D reprojection error
    eps          = 1e-5
    iou_test_c   = len(np.where(np.array(iou_convex_acc) >= 0.5)[0]) * 100 / (len(iou_convex_acc) + eps)
    iou_test25   = len(np.where(np.array(iou_acc) >= 0.25)[0]) * 100 / (len(iou_acc) + eps)
    iou_test     = len(np.where(np.array(iou_acc) >= 0.5)[0]) * 100 / (len(iou_acc) + eps)
    iou_test75   = len(np.where(np.array(iou_acc) >= 0.75)[0]) * 100 / (len(iou_acc) + eps)
    proj_test05  = len(np.where(np.array(errs_2d) <= 5)[0]) * 100. / (len(errs_2d)+eps)
    proj_test    = len(np.where(np.array(errs_2d) <= px_threshold)[0]) * 100. / (len(errs_2d)+eps)
    proj_test15  = len(np.where(np.array(errs_2d) <= 15)[0]) * 100. / (len(errs_2d)+eps)
    proj_test20  = len(np.where(np.array(errs_2d) <= 20)[0]) * 100. / (len(errs_2d)+eps)
    nts = float(testing_samples)

    # Print test statistics
    logging('Results of {} ({}):'.format(name, datetime.datetime.now()))
    logging('   Mean 2D Err. (Pixel Dist.) = {:.2f} pix.'.format(testing_error_pixel/nts))
    logging('   Acc. using  5 px. 2D Projection = {:.2f}%'.format(proj_test05))
    logging('   Acc. using {} px. 2D Projection = {:.2f}%'.format(px_threshold, proj_test))
    logging('   Acc. using 15 px. 2D Projection = {:.2f}%'.format(proj_test15))
    logging('   Acc. using 20 px. 2D Projection = {:.2f}%'.format(proj_test20))
    logging('   Acc. using Intersection Of Union (IoU, convex) = {:.2f}%'.format(iou_test_c))
    if proj==True: logging('   Acc. using Intersection Of Union (IoU > 0.25) = {:.2f}%'.format(iou_test25))
    if proj==True: logging('   Acc. using Intersection Of Union (IoU > 0.50) = {:.2f}%'.format(iou_test))
    if proj==True: logging('   Acc. using Intersection Of Union (IoU > 0.75) = {:.2f}%'.format(iou_test75))
    logging('Reproj. test: {:.2f}%, IoU test: {:.2f}%'.format(proj_test20, iou_test_c))

    if save:
        fid = open("experimental_results/{}.txt".format(name), "w")
        fid.write("{:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f}".format( testing_error_pixel/nts, proj_test05, proj_test, proj_test15, proj_test20, iou_test_c, iou_test25, iou_test, iou_test75))
        fid.close()

if __name__ == '__main__':
    # Parse configuration files
    parser = argparse.ArgumentParser(description='SingleShotPose')
    parser.add_argument('--datacfg', type=str, default='data/070308/070308.data') # data config
    parser.add_argument('--modelcfg', type=str, default='data/070308/models/yolo-pose.cfg') # network config
    parser.add_argument('--weightfile', type=str, default='data/070308/models/model.weights') # imagenet initialized weights
    args       = parser.parse_args()
    datacfg    = args.datacfg
    modelcfg   = args.modelcfg
    weightfile = args.weightfile
    valid(datacfg, modelcfg, weightfile)
