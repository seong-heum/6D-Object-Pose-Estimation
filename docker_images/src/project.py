import cv2 as cv
from utils import *
from MeshPly import MeshPly

if __name__ == '__main__':
    name = "100211"
    valid_images = "data/{}/test.txt".format(name)
    backupdir = "data/{}/models".format(name)
    meshname = "data/{}/{}.ply".format(name, name)

    mesh  = MeshPly(meshname)
    vertices = np.c_[np.array(mesh.vertices), np.ones((len(mesh.vertices), 1))].transpose()
    indices = np.c_[np.array(mesh.indices), np.ones((len(mesh.indices), 2))].transpose()
    corners3D = get_3D_corners(vertices)

    with open(valid_images) as fp:
        tmp_files = fp.readlines()
        valid_files = [item.rstrip() for item in tmp_files]

    for k in range(valid_files.__len__()):
        print(valid_files[k])
        f_cam = open("data/{}/cams/{}.txt".format(name, valid_files[k][-17:-4]))
        rdata = f_cam.readlines()
        [fx, fy, u0, v0] = rdata[0].split(" ")
        [fx, fy, u0, v0] = [float(fx), float(fy), float(u0), float(v0)]
        f_cam.close()
        intrinsic_calibration = get_camera_intrinsic(u0, v0, fx, fy)

        #labels = np.loadtxt("data/{}/labels/{}_{}.txt".format(name, name, valid_files[k][-10:-4]))
        #corners2D = np.zeros((9,2))
        #corners2D[0][0] = labels[1] * 1280; corners2D[0][1] = labels[2] * 720;
        #corners2D[1][0] = labels[3] * 1280; corners2D[1][1] = labels[4] * 720;
        #corners2D[2][0] = labels[5] * 1280; corners2D[2][1] = labels[6] * 720;
        #corners2D[3][0] = labels[7] * 1280; corners2D[3][1] = labels[8] * 720;
        #corners2D[4][0] = labels[9] * 1280; corners2D[4][1] = labels[10] * 720;
        #corners2D[5][0] = labels[11] * 1280; corners2D[5][1] = labels[12] * 720;
        #corners2D[6][0] = labels[13] * 1280; corners2D[6][1] = labels[14] * 720;
        #corners2D[7][0] = labels[15] * 1280; corners2D[7][1] = labels[16] * 720;
        #corners2D[8][0] = labels[17] * 1280; corners2D[8][1] = labels[18] * 720;
        #R_gt, t_gt = pnp(np.array(np.transpose(np.concatenate((np.zeros((3, 1)), corners3D[:3, :]), axis=1)), dtype='float32'), corners2D, np.array(intrinsic_calibration, dtype='float32'))
        #Rt_gt = np.concatenate((R_gt, t_gt), axis=1)
        #proj_corners2D_gt = np.transpose(compute_projection(corners3D, Rt_gt, intrinsic_calibration))
        #err = proj_corners2D_gt - corners2D[1:, :]

        K = np.array([[fx, 0, u0], [0, fy, v0], [0, 0, 1]])
        R = np.loadtxt("data/{}/models/test/pr/R_{}.txt".format(name, valid_files[k][-8:-4]))
        t = np.loadtxt("data/{}/models/test/pr/t_{}.txt".format(name, valid_files[k][-8:-4]))
        P = np.vstack([R.T, t]).T

        f_prj = open("data/{}/models/test/pr/prj_{}.txt".format(name, valid_files[k][-8:-4]), 'w')
        for i in range(vertices.shape[1]):
            p_n = P @ np.transpose(vertices[:,i])
            p = K @ np.transpose([ p_n[0]/p_n[2], p_n[1]/p_n[2], 1 ])
            p_x = int(p[0]/p[2]+0.5)
            p_y = int(p[1]/p[2]+0.5)
            f_prj.write("{} {}\n".format(p_x, p_y))
        f_prj.close()

        f_ind = open("data/{}/models/test/pr/ind_{}.txt".format(name, valid_files[k][-8:-4]), 'w')
        for j in range(indices.shape[1]):
            f_ind.write("{} {} {}\n".format(int(indices[0,j]), int(indices[1,j]), int(indices[2,j])))
        f_ind.close()