import argparse
import numpy as np
import cv2 as cv
import random
from utils import *
from MeshPly import MeshPly

if __name__ == '__main__':
    # Parse configuration files
    parser = argparse.ArgumentParser(description='SingleShotPose')
    parser.add_argument('--datacfg', type=str, default='data/070308/070308.data')  # data config
    args = parser.parse_args()
    datacfg = args.datacfg

    data_options = read_data_cfg(datacfg)
    valid_images = data_options['valid']
    meshname = data_options['mesh']
    name = data_options['name']

    mesh = MeshPly(meshname)
    vertices = np.c_[np.array(mesh.vertices), np.ones((len(mesh.vertices), 1))].transpose()
    indices = np.c_[np.array(mesh.indices), np.ones((len(mesh.indices), 2))].transpose()
    corners3D = get_3D_corners(vertices)

    with open(valid_images) as fp:
        tmp_files = fp.readlines()
        valid_files = [item.rstrip() for item in tmp_files]

    if (os.path.isdir("experimental_results") == 0): os.mkdir("experimental_results")
    if (os.path.isdir("experimental_results/" + name + "_check") == 0): os.mkdir("experimental_results/" + name + "_check")
    if (os.path.isdir("data/" + name + "/check") == 0): os.mkdir("data/" + name + "/check")

    rep_acc = []
    iou_acc = []

    nts = len(valid_files)
    file = open("experimental_results/{}_check/{}_check.txt".format(name, name), "w")
    for count in range(0,nts):
    #for count in range(0,5):

        #rind = random.randint(0, nts-1)
        #frame = valid_files[rind][-8:-4]
        frame = valid_files[count][-8:-4]

        img = cv2.imread("data/{}/images/{}_00{}.png".format(name, name, frame))
        f_cam = open("data/{}/cams/{}_00{}.txt".format(name, name, frame))
        rdata = f_cam.readlines()
        [fx, fy, u0, v0] = rdata[0].split(" ")
        [fx, fy, u0, v0] = [float(fx), float(fy), float(u0), float(v0)]
        f_cam.close()
        intrinsic_calibration = get_camera_intrinsic(u0, v0, fx, fy)

        labels = np.loadtxt("data/{}/labels/{}_00{}.txt".format(name, name, frame))
        x1 = labels[3] * 1280;
        y1 = labels[4] * 720;
        x2 = labels[5] * 1280;
        y2 = labels[6] * 720;
        x3 = labels[7] * 1280;
        y3 = labels[8] * 720;
        x4 = labels[9] * 1280;
        y4 = labels[10] * 720;
        x5 = labels[11] * 1280;
        y5 = labels[12] * 720;
        x6 = labels[13] * 1280;
        y6 = labels[14] * 720;
        x7 = labels[15] * 1280;
        y7 = labels[16] * 720;
        x8 = labels[17] * 1280;
        y8 = labels[18] * 720;
        cv2.line(img, (int(x1), int(y1)), (int(x1), int(y1)), [0, 255, 0], 10)
        cv2.line(img, (int(x2), int(y2)), (int(x2), int(y2)), [0, 255, 0], 10)
        cv2.line(img, (int(x3), int(y3)), (int(x3), int(y3)), [0, 255, 0], 10)
        cv2.line(img, (int(x4), int(y4)), (int(x4), int(y4)), [0, 255, 0], 10)
        cv2.line(img, (int(x5), int(y5)), (int(x5), int(y5)), [0, 255, 0], 10)
        cv2.line(img, (int(x6), int(y6)), (int(x6), int(y6)), [0, 255, 0], 10)
        cv2.line(img, (int(x7), int(y7)), (int(x7), int(y7)), [0, 255, 0], 10)
        cv2.line(img, (int(x8), int(y8)), (int(x8), int(y8)), [0, 255, 0], 10)
        cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), [0, 255, 0], 2)
        cv2.line(img, (int(x1), int(y1)), (int(x3), int(y3)), [0, 255, 0], 2)
        cv2.line(img, (int(x2), int(y2)), (int(x4), int(y4)), [0, 255, 0], 2)
        cv2.line(img, (int(x3), int(y3)), (int(x4), int(y4)), [0, 255, 0], 2)
        cv2.line(img, (int(x5), int(y5)), (int(x6), int(y6)), [0, 255, 0], 2)
        cv2.line(img, (int(x5), int(y5)), (int(x7), int(y7)), [0, 255, 0], 2)
        cv2.line(img, (int(x6), int(y6)), (int(x8), int(y8)), [0, 255, 0], 2)
        cv2.line(img, (int(x7), int(y7)), (int(x8), int(y8)), [0, 255, 0], 2)
        cv2.line(img, (int(x1), int(y1)), (int(x5), int(y5)), [0, 255, 0], 2)
        cv2.line(img, (int(x2), int(y2)), (int(x6), int(y6)), [0, 255, 0], 2)
        cv2.line(img, (int(x3), int(y3)), (int(x7), int(y7)), [0, 255, 0], 2)
        cv2.line(img, (int(x4), int(y4)), (int(x8), int(y8)), [0, 255, 0], 2)
        cv2.putText(img, '1', (int(x1) + 10, int(y1) + 10), cv2.FONT_HERSHEY_PLAIN, 3, [255, 0, 0], 3)
        cv2.putText(img, '2', (int(x2) + 10, int(y2) + 10), cv2.FONT_HERSHEY_PLAIN, 3, [255, 0, 0], 3)
        cv2.putText(img, '3', (int(x3) + 10, int(y3) + 10), cv2.FONT_HERSHEY_PLAIN, 3, [255, 0, 0], 3)
        cv2.putText(img, '4', (int(x4) + 10, int(y4) + 10), cv2.FONT_HERSHEY_PLAIN, 3, [255, 0, 0], 3)
        cv2.putText(img, '5', (int(x5) + 10, int(y5) + 10), cv2.FONT_HERSHEY_PLAIN, 3, [255, 0, 0], 3)
        cv2.putText(img, '6', (int(x6) + 10, int(y6) + 10), cv2.FONT_HERSHEY_PLAIN, 3, [255, 0, 0], 3)
        cv2.putText(img, '7', (int(x7) + 10, int(y7) + 10), cv2.FONT_HERSHEY_PLAIN, 3, [255, 0, 0], 3)
        cv2.putText(img, '8', (int(x8) + 10, int(y8) + 10), cv2.FONT_HERSHEY_PLAIN, 3, [255, 0, 0], 3)

        corners2D = np.zeros((9, 2))
        corners2D[0][0] = labels[1] * 1280;
        corners2D[0][1] = labels[2] * 720;
        corners2D[1][0] = labels[3] * 1280;
        corners2D[1][1] = labels[4] * 720;
        corners2D[2][0] = labels[5] * 1280;
        corners2D[2][1] = labels[6] * 720;
        corners2D[3][0] = labels[7] * 1280;
        corners2D[3][1] = labels[8] * 720;
        corners2D[4][0] = labels[9] * 1280;
        corners2D[4][1] = labels[10] * 720;
        corners2D[5][0] = labels[11] * 1280;
        corners2D[5][1] = labels[12] * 720;
        corners2D[6][0] = labels[13] * 1280;
        corners2D[6][1] = labels[14] * 720;
        corners2D[7][0] = labels[15] * 1280;
        corners2D[7][1] = labels[16] * 720;
        corners2D[8][0] = labels[17] * 1280;
        corners2D[8][1] = labels[18] * 720;

        R_gt, t_gt = pnp(np.array(np.transpose(np.concatenate((np.zeros((3, 1)), corners3D[:3, :]), axis=1)), dtype='float32'), corners2D, np.array(intrinsic_calibration, dtype='float32'))
        Rt_gt = np.concatenate((R_gt, t_gt), axis=1)
        corners2Dp = np.transpose(compute_projection(corners3D, Rt_gt, intrinsic_calibration))
        rep = np.mean(np.linalg.norm(corners2D[1:9,:]-corners2Dp, axis=1))
        rep_acc.append(rep)
        cv2.line(img, (int(corners2Dp[0][0]), int(corners2Dp[0][1])), (int(corners2Dp[1][0]), int(corners2Dp[1][1])), [255,0,255], 2)
        cv2.line(img, (int(corners2Dp[0][0]), int(corners2Dp[0][1])), (int(corners2Dp[2][0]), int(corners2Dp[2][1])), [255,0,255], 2)
        cv2.line(img, (int(corners2Dp[1][0]), int(corners2Dp[1][1])), (int(corners2Dp[3][0]), int(corners2Dp[3][1])), [255,0,255], 2)
        cv2.line(img, (int(corners2Dp[2][0]), int(corners2Dp[2][1])), (int(corners2Dp[3][0]), int(corners2Dp[3][1])), [255,0,255], 2)
        cv2.line(img, (int(corners2Dp[0][0]), int(corners2Dp[0][1])), (int(corners2Dp[4][0]), int(corners2Dp[4][1])), [255,0,255], 2)
        cv2.line(img, (int(corners2Dp[1][0]), int(corners2Dp[1][1])), (int(corners2Dp[5][0]), int(corners2Dp[5][1])), [255,0,255], 2)
        cv2.line(img, (int(corners2Dp[2][0]), int(corners2Dp[2][1])), (int(corners2Dp[6][0]), int(corners2Dp[6][1])), [255,0,255], 2)
        cv2.line(img, (int(corners2Dp[3][0]), int(corners2Dp[3][1])), (int(corners2Dp[7][0]), int(corners2Dp[7][1])), [255,0,255], 2)
        cv2.line(img, (int(corners2Dp[4][0]), int(corners2Dp[4][1])), (int(corners2Dp[5][0]), int(corners2Dp[5][1])), [255,0,255], 2)
        cv2.line(img, (int(corners2Dp[4][0]), int(corners2Dp[4][1])), (int(corners2Dp[6][0]), int(corners2Dp[6][1])), [255,0,255], 2)
        cv2.line(img, (int(corners2Dp[5][0]), int(corners2Dp[5][1])), (int(corners2Dp[7][0]), int(corners2Dp[7][1])), [255,0,255], 2)
        cv2.line(img, (int(corners2Dp[6][0]), int(corners2Dp[6][1])), (int(corners2Dp[7][0]), int(corners2Dp[7][1])), [255,0,255], 2)

        np.savetxt("data/{}/check/{}_{}_R.txt".format(name, name, frame), np.array(R_gt, dtype='float32'))
        np.savetxt("data/{}/check/{}_{}_t.txt".format(name, name, frame), np.array(t_gt, dtype='float32'))
        K = np.array([[fx, 0, u0], [0, fy, v0], [0, 0, 1]])
        R = np.loadtxt("data/{}/check/{}_{}_R.txt".format(name, name, frame))
        t = np.loadtxt("data/{}/check/{}_{}_t.txt".format(name, name, frame))
        RT = np.vstack([R.T, t]).T
        f_prj = open("data/{}/check/{}_{}_prj.txt".format(name, name, frame), 'w')
        for i in range(vertices.shape[1]):
            p_n = RT @ np.transpose(vertices[:, i])
            p = K @ np.transpose([p_n[0] / p_n[2], p_n[1] / p_n[2], 1])
            p_x = int(p[0] / p[2] + 0.5)
            p_y = int(p[1] / p[2] + 0.5)
            f_prj.write("{} {}\n".format(p_x, p_y))
        f_prj.close()

        f_ind = open("data/{}/check/{}_{}_ind.txt".format(name, name, frame), 'w')
        for j in range(indices.shape[1]):
            f_ind.write("{} {} {}\n".format(int(indices[0, j]), int(indices[1, j]), int(indices[2, j])))
        f_ind.close()

        # Compute IoU
        iou = compute_iou(name, frame, 2)
        iou_acc.append(iou)
        gmask = cv.imread("data/{}/masks/{}_00{}.png".format(name, name, frame),0)
        pmask = cv.imread("data/{}/check/{}_{}_pmask.png".format(name, name, frame),0)
        # emask = np.zeros((720, 1280, 1), dtype=np.uint8)
        RGB = cv.merge((pmask, gmask, pmask))

        cv.imwrite("experimental_results/{}_check/rep_test_{}_{}.png".format(name, name, frame), img)
        cv.imwrite("experimental_results/{}_check/iou_test_{}_{}.png".format(name, name, frame), RGB)
        file.write("{}: {:>10.2f} (rep_test) {:>10.2f} (iou_test)".format(frame, rep, iou))
        file.write("\n")
    file.close()

    eps = 1e-5
    rep_test05 = len(np.where(np.array(rep_acc) <= 5)[0]) * 100. / (len(rep_acc) + eps)
    rep_test10 = len(np.where(np.array(rep_acc) <= 10)[0]) * 100. / (len(rep_acc) + eps)
    rep_test15 = len(np.where(np.array(rep_acc) <= 15)[0]) * 100. / (len(rep_acc) + eps)
    iou_test25 = len(np.where(np.array(iou_acc) >= 0.25)[0]) * 100 / (len(iou_acc) + eps)
    iou_test50 = len(np.where(np.array(iou_acc) >= 0.50)[0]) * 100 / (len(iou_acc) + eps)
    iou_test75 = len(np.where(np.array(iou_acc) >= 0.75)[0]) * 100 / (len(iou_acc) + eps)
    file = open("experimental_results/{}_check.txt".format(name), "w")
    file.write("{:>10.2f} {:>10.2f} {:>10.2f} {:>10.2f} {:>10.2f} {:>10.2f}".format(rep_test05, rep_test10, rep_test15, iou_test25, iou_test50, iou_test75))
    file.close()

    file = open("experimental_results/{}_check/{}_check_summary.txt".format(name, name), "w")
    file.write("{:>10.2f} {:>10.2f} {:>10.2f} {:>10.2f} {:>10.2f} {:>10.2f}".format(rep_test05, rep_test10, rep_test15, iou_test25, iou_test50, iou_test75))
    file.close()
    print("{}: {:>10.2f} {:>10.2f} {:>10.2f} {:>10.2f} {:>10.2f} {:>10.2f}".format(rep_test05, rep_test10, rep_test15, iou_test25, iou_test50, iou_test75))