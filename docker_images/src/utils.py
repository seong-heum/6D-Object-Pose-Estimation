import sys
import os
import time
import math
import torch
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from torch.autograd import Variable
import torch.nn.functional as F
import cv2
from scipy import spatial

import struct 
import imghdr 

def id2eng(id):
    class_dict = {'0101':'0101',
                  '0102':'0102',
                  '0301':'0301',
                  '0302':'0302',
                  '0303':'0303',
                  '0403':'0403',
                  '0404':'0404',
                  '0501':'0501',
                  '0502':'0502',
                  '0503':'0503',
                  '0601':'0601',
                  '0602':'0602',
                  '0603':'0603',
                  '0701':'0701',
                  '0702':'0702',
                  '0703':'0703',
                  '0704':'0704',
                  '0705':'0705',
                  '0706':'0706',
                  '0707':'0707',
                  '0708':'0708',
                  '0709':'0709',
                  '0710':'0710',
                  '0801':'0801',
                  '0901':'0901',
                  '0902':'0902',
                  '0903':'0903',
                  '0904':'0904',
                  '0905':'0905',
                  '1001':'1001',
                  '1002':'1002',
                  '1101':'1101'}
    return class_dict[id[:4]] + str(int(id[-2:]))

def id2kor(id):
    class_dict = {'0101':'0101',
                  '0102':'0102',
                  '0301':'0301',
                  '0302':'0302',
                  '0303':'0303',
                  '0403':'0403',
                  '0404':'0404',
                  '0501':'0501',
                  '0502':'0502',
                  '0503':'0503',
                  '0601':'0601',
                  '0602':'0602',
                  '0603':'0603',
                  '0701':'0701',
                  '0702':'0702',
                  '0703':'0703',
                  '0704':'0704',
                  '0705':'0705',
                  '0706':'0706',
                  '0707':'0707',
                  '0708':'0708',
                  '0709':'0709',
                  '0710':'0710',
                  '0801':'0801',
                  '0901':'0901',
                  '0902':'0902',
                  '0903':'0903',
                  '0904':'0904',
                  '0905':'0905',
                  '1001':'1001',
                  '1002':'1002',
                  '1101':'1101'}
    return class_dict[id[:4]] + str(int(id[-2:]))

# Create new directory
def makedirs(path):
    if not os.path.exists( path ):
        os.makedirs( path )

def get_all_files(directory):
    files = []

    for f in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, f)):
            files.append(os.path.join(directory, f))
        else:
            files.extend(get_all_files(os.path.join(directory, f)))
    return files

def calcAngularDistance(gt_rot, pr_rot):

    rotDiff = np.dot(gt_rot, np.transpose(pr_rot))
    trace = np.trace(rotDiff) 
    return np.rad2deg(np.arccos((trace-1.0)/2.0))

def get_camera_intrinsic(u0, v0, fx, fy):
    return np.array([[fx, 0.0, u0], [0.0, fy, v0], [0.0, 0.0, 1.0]])

def compute_projection(points_3D, transformation, internal_calibration):
    projections_2d = np.zeros((2, points_3D.shape[1]), dtype='float32')
    camera_projection = (internal_calibration.dot(transformation)).dot(points_3D)
    projections_2d[0, :] = camera_projection[0, :]/camera_projection[2, :]
    projections_2d[1, :] = camera_projection[1, :]/camera_projection[2, :]
    return projections_2d

def compute_transformation(points_3D, transformation):
    return transformation.dot(points_3D)

def calc_pts_diameter(pts):
    diameter = -1
    for pt_id in range(pts.shape[0]):
        pt_dup = np.tile(np.array([pts[pt_id, :]]), [pts.shape[0] - pt_id, 1])
        pts_diff = pt_dup - pts[pt_id:, :]
        max_dist = math.sqrt((pts_diff * pts_diff).sum(axis=1).max())
        if max_dist > diameter:
            diameter = max_dist
    return diameter

def adi(pts_est, pts_gt):
    nn_index = spatial.cKDTree(pts_est)
    nn_dists, _ = nn_index.query(pts_gt, k=1)
    e = nn_dists.mean()
    return e

def get_3D_corners(vertices):
    
    min_x = np.min(vertices[0,:])
    max_x = np.max(vertices[0,:])
    min_y = np.min(vertices[1,:])
    max_y = np.max(vertices[1,:])
    min_z = np.min(vertices[2,:])
    max_z = np.max(vertices[2,:])
    corners = np.array([[min_x, min_y, min_z],
                        [min_x, min_y, max_z],
                        [min_x, max_y, min_z],
                        [min_x, max_y, max_z],
                        [max_x, min_y, min_z],
                        [max_x, min_y, max_z],
                        [max_x, max_y, min_z],
                        [max_x, max_y, max_z]])

    corners = np.concatenate((np.transpose(corners), np.ones((1,8)) ), axis=0)
    return corners

def pnp(points_3D, points_2D, cameraMatrix):
    try:
        distCoeffs = pnp.distCoeffs
    except:
        distCoeffs = np.zeros((8, 1), dtype='float32') 

    assert points_2D.shape[0] == points_2D.shape[0], 'points 3D and points 2D must have same number of vertices'

    _, R_exp, t = cv2.solvePnP(points_3D,
                              np.ascontiguousarray(points_2D[:,:2]).reshape((-1,1,2)),
                              cameraMatrix,
                              distCoeffs)                            

    R, _ = cv2.Rodrigues(R_exp)
    return R, t

def get_2d_bb(box, size):
    x = box[0]
    y = box[1]
    min_x = np.min(np.reshape(box, [-1,2])[:,0])
    max_x = np.max(np.reshape(box, [-1,2])[:,0])
    min_y = np.min(np.reshape(box, [-1,2])[:,1])
    max_y = np.max(np.reshape(box, [-1,2])[:,1])
    w = max_x - min_x
    h = max_y - min_y
    new_box = [x*size, y*size, w*size, h*size]
    return new_box

def compute_2d_bb(pts):
    min_x = np.min(pts[0,:])
    max_x = np.max(pts[0,:])
    min_y = np.min(pts[1,:])
    max_y = np.max(pts[1,:])
    w  = max_x - min_x
    h  = max_y - min_y
    cx = (max_x + min_x) / 2.0
    cy = (max_y + min_y) / 2.0
    new_box = [cx, cy, w, h]
    return new_box


def ccw(p1, p2, p3):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    result = ((x1 * y2 + x2 * y3 + x3 * y1) - (x2 * y1 + x3 * y2 + x1 * y3))
    return result


def get_cross_point(gt1, gt2, pr1, pr2):
    p = []
    m_gt = (gt1[1] - gt2[1]) / (gt1[0] - gt2[0])
    m_pr = (pr1[1] - pr2[1]) / (pr1[0] - pr2[0])
    x = ((m_gt * gt2[0]) - (m_pr * pr2[0]) + pr2[1] - gt2[1]) / (m_gt - m_pr)
    y = m_gt * (x - gt2[0]) + gt2[1]
    if gt1[0] == gt2[0]:
        x = gt1[0]
        y = (m_pr * (gt1[0] - pr2[0]) + pr2[1])
    if gt1[1] == gt2[1]:
        x = ((gt1[1] - pr2[1]) / m_pr) + pr2[0]
        y = gt1[1]
    p.append(x)
    p.append(y)
    return p


def compute_inner_point(gt, pr):
    inner_point = []
    n = 0
    z = [0, 0]
    hull_gt = spatial.ConvexHull(gt)
    hull_pr = spatial.ConvexHull(pr)
    x = hull_gt.points
    y = hull_pr.points
    u = hull_gt.vertices
    v = hull_pr.vertices

    for i in range(len(u)):
        for j in range(len(v)):
            if (ccw(z, x[u[i]], y[v[j - 1]]) * ccw(z, x[u[i]], y[v[j]])) < 0:
                if (ccw(y[v[j - 1]], y[v[j]], z) * ccw(y[v[j - 1]], y[v[j]], x[u[i]])) < 0:
                    n = n + 1
        if n % 2 == 1:
            inner_point.append(x[u[i]][0])
            inner_point.append(x[u[i]][1])
            n = 0

    for j in range(len(v)):
        for i in range(len(u)):
            if ((ccw(z, y[v[j]], x[u[i - 1]]) * ccw(z, y[v[j]], x[u[i]])) < 0):
                if ((ccw(x[u[i - 1]], x[u[i]], z) * ccw(x[u[i - 1]], x[u[i]], y[v[j]])) < 0):
                    n = n + 1
        if n % 2 == 1:
            inner_point.append(y[v[j]][0])
            inner_point.append(y[v[j]][1])
            n = 0

    return inner_point


def compute_cross_point(gt, pr):
    cross_point = []
    p = []
    hull_gt = spatial.ConvexHull(gt)
    hull_pr = spatial.ConvexHull(pr)
    x = hull_gt.points
    y = hull_pr.points
    u = hull_gt.vertices
    v = hull_pr.vertices

    for i in range(len(u)):
        for j in range(len(v)):
            if (ccw(x[u[i - 1]], x[u[i]], y[v[j - 1]]) * ccw(x[u[i - 1]], x[u[i]], y[v[j]])) < 0:
                if (ccw(y[v[j - 1]], y[v[j]], x[u[i - 1]]) * ccw(y[v[j - 1]], y[v[j]], x[u[i]])) < 0:
                    p = get_cross_point(x[u[i - 1]], x[u[i]], y[v[j - 1]], y[v[j]])
                    cross_point = cross_point + p

    return cross_point


def visualize(name, frame, corners3D):
    img = cv2.imread("data/{}/images/{}_00{}.png".format(name, name, frame))
    cube = np.loadtxt("data/{}/models/vis/corners_{}.txt".format(name, frame))

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
    cv2.line(img, (int(corners2Dp[0][0]), int(corners2Dp[0][1])), (int(corners2Dp[1][0]), int(corners2Dp[1][1])), [0,255,255], 2)
    cv2.line(img, (int(corners2Dp[0][0]), int(corners2Dp[0][1])), (int(corners2Dp[2][0]), int(corners2Dp[2][1])), [0,255,255], 2)
    cv2.line(img, (int(corners2Dp[1][0]), int(corners2Dp[1][1])), (int(corners2Dp[3][0]), int(corners2Dp[3][1])), [0,255,255], 2)
    cv2.line(img, (int(corners2Dp[2][0]), int(corners2Dp[2][1])), (int(corners2Dp[3][0]), int(corners2Dp[3][1])), [0,255,255], 2)
    cv2.line(img, (int(corners2Dp[0][0]), int(corners2Dp[0][1])), (int(corners2Dp[4][0]), int(corners2Dp[4][1])), [0,255,255], 2)
    cv2.line(img, (int(corners2Dp[1][0]), int(corners2Dp[1][1])), (int(corners2Dp[5][0]), int(corners2Dp[5][1])), [0,255,255], 2)
    cv2.line(img, (int(corners2Dp[2][0]), int(corners2Dp[2][1])), (int(corners2Dp[6][0]), int(corners2Dp[6][1])), [0,255,255], 2)
    cv2.line(img, (int(corners2Dp[3][0]), int(corners2Dp[3][1])), (int(corners2Dp[7][0]), int(corners2Dp[7][1])), [0,255,255], 2)
    cv2.line(img, (int(corners2Dp[4][0]), int(corners2Dp[4][1])), (int(corners2Dp[5][0]), int(corners2Dp[5][1])), [0,255,255], 2)
    cv2.line(img, (int(corners2Dp[4][0]), int(corners2Dp[4][1])), (int(corners2Dp[6][0]), int(corners2Dp[6][1])), [0,255,255], 2)
    cv2.line(img, (int(corners2Dp[5][0]), int(corners2Dp[5][1])), (int(corners2Dp[7][0]), int(corners2Dp[7][1])), [0,255,255], 2)
    cv2.line(img, (int(corners2Dp[6][0]), int(corners2Dp[6][1])), (int(corners2Dp[7][0]), int(corners2Dp[7][1])), [0,255,255], 2)

    # prediction
    cv2.line(img, (int(cube[1][0]), int(cube[1][1])), (int(cube[2][0]), int(cube[2][1])), [255,0,0], 2)
    cv2.line(img, (int(cube[1][0]), int(cube[1][1])), (int(cube[3][0]), int(cube[3][1])), [255,0,0], 2)
    cv2.line(img, (int(cube[2][0]), int(cube[2][1])), (int(cube[4][0]), int(cube[4][1])), [255,0,0], 2)
    cv2.line(img, (int(cube[3][0]), int(cube[3][1])), (int(cube[4][0]), int(cube[4][1])), [255,0,0], 2)
    cv2.line(img, (int(cube[1][0]), int(cube[1][1])), (int(cube[5][0]), int(cube[5][1])), [255,0,0], 2)
    cv2.line(img, (int(cube[2][0]), int(cube[2][1])), (int(cube[6][0]), int(cube[6][1])), [255,0,0], 2)
    cv2.line(img, (int(cube[3][0]), int(cube[3][1])), (int(cube[7][0]), int(cube[7][1])), [255,0,0], 2)
    cv2.line(img, (int(cube[4][0]), int(cube[4][1])), (int(cube[8][0]), int(cube[8][1])), [255,0,0], 2)
    cv2.line(img, (int(cube[5][0]), int(cube[5][1])), (int(cube[6][0]), int(cube[6][1])), [255,0,0], 2)
    cv2.line(img, (int(cube[5][0]), int(cube[5][1])), (int(cube[7][0]), int(cube[7][1])), [255,0,0], 2)
    cv2.line(img, (int(cube[6][0]), int(cube[6][1])), (int(cube[8][0]), int(cube[8][1])), [255,0,0], 2)
    cv2.line(img, (int(cube[7][0]), int(cube[7][1])), (int(cube[8][0]), int(cube[8][1])), [255,0,0], 2)
    cv2.imwrite("data/{}/models/vis/cube_{}.png".format(name, frame), img)


def compute_iou(name, frame, vis):

    sz = [720, 1280]
    if vis==1:
        proj = np.loadtxt("data/{}/models/vis/prj_{}.txt".format(name, frame))
        face = np.loadtxt("data/{}/models/vis/ind_{}.txt".format(name, frame))
    elif vis==2:
        proj = np.loadtxt("data/{}/check/{}_{}_prj.txt".format(name, name, frame))
        face = np.loadtxt("data/{}/check/{}_{}_ind.txt".format(name, name, frame))

    proj[:,0] = np.clip(np.floor(proj[:,0]+0.5),0,sz[1]-1)
    proj[:,1] = np.clip(np.floor(proj[:,1]+0.5),0,sz[0]-1)
    face = np.uint32(face)

    proj1 = np.double(proj[face[:,0],:])
    proj2 = np.double(proj[face[:,1],:])
    proj3 = np.double(proj[face[:,2],:])

    tr = np.concatenate( (proj1,proj2-proj1,proj3-proj1), axis=1 )
    d0 = tr[:,2] * tr[:,5] - tr[:,3] * tr[:,4]
    d1 = tr[:,0] * tr[:,5] - tr[:,1] * tr[:,4]
    d2 = tr[:,0] * tr[:,3] - tr[:,1] * tr[:,2]
    vec = np.column_stack((tr,d0,d1,d2))

    n = face.shape[0]
    zbuffer = np.zeros( (sz[0],sz[1]) )

    # zbuffer
    for k in range(0, n):
        v0 = vec[k,0:2]; v1 = vec[k,2:4]; v2 = vec[k,4:6];
        d0 = vec[k,6];   d1 = vec[k,7];   d2 = vec[k,8];
        v1_ = v1 + v0
        v2_ = v2 + v0

        vmax = np.max(np.row_stack((v0,v1_,v2_)) ,axis=0)
        vmin = np.min(np.row_stack((v0,v1_,v2_)) ,axis=0)
        vmin[0] = np.clip(np.floor(vmin[0]),0,sz[1]-1)
        vmin[1] = np.clip(np.floor(vmin[1]),0,sz[0]-1)
        vmax[0] = np.clip(np.floor(vmax[0]),0,sz[1]-1)
        vmax[1] = np.clip(np.floor(vmax[1]),0,sz[0]-1)
        sz_k = vmax - vmin

        x,y = np.meshgrid(np.linspace(vmin[0],vmax[0],np.uint32(vmax[0]-vmin[0]+1)),np.linspace(vmin[1],vmax[1],np.uint32(vmax[1]-vmin[1]+1)))
        x_,y_ = x.T.flatten(), y.T.flatten()

        if d0 == 0:
            mask = np.zeros((np.int(sz_k[1]) + 1, np.int(sz_k[0]) + 1))
        else:
            a = ((x_*v2[1] - y_*v2[0]) - d1) / d0
            b = - (x_*v1[1] - y_*v1[0] - d2) / d0
            mask = (a>=0) & (b>=0) & (a+b<=1)
            mask = mask.reshape(np.int(sz_k[1]+1), np.int(sz_k[0]+1), order='F').copy()

        ind1,ind2,ind3 = np.zeros(2,'int32'), np.zeros(2,'int32'), np.zeros(2,'int32')
        ind1[0] = np.int32(np.clip(v0[0]-vmin[0],0,sz_k[0]))
        ind1[1] = np.int32(np.clip(v0[1]-vmin[1],0,sz_k[1]))
        ind2[0] = np.int32(np.clip(v1_[0]-vmin[0],0,sz_k[0]))
        ind2[1] = np.int32(np.clip(v1_[1]-vmin[1],0,sz_k[1]))
        ind3[0] = np.int32(np.clip(v2_[0]-vmin[0],0,sz_k[0]))
        ind3[1] = np.int32(np.clip(v2_[1]-vmin[1],0,sz_k[1]))
        mask[ind1[1],ind1[0]] = 1
        mask[ind2[1],ind2[0]] = 1
        mask[ind3[1],ind3[0]] = 1
        ind = np.where( (mask>0) )

        zbuffer_k = zbuffer[np.int32(vmin[1]):np.int32(vmax[1]+1),np.int32(vmin[0]):np.int32(vmax[0]+1)]
        zbuffer_k[ ind[0], ind[1] ] = k+1
        zbuffer[np.int32(vmin[1]):np.int32(vmax[1]+1),np.int32(vmin[0]):np.int32(vmax[0]+1)] = zbuffer_k

    pmask = zbuffer > 0 # zbuffer --> mask

    # compute IoU score
    gmask = cv2.imread("data/{}/masks/{}_00{}.png".format(name, name, frame),0)
    gmask_ = np.bool_(gmask/255)
    mask1 = pmask & gmask_
    mask2 = pmask | gmask_
    ind1 = np.where(mask1==1)
    ind2 = np.where(mask2==1)
    iou = len(ind1[0])/len(ind2[0])

    if vis==1:
        pmask_ = np.uint8(pmask)
        cv2.imwrite("data/{}/models/vis/mask_{}.png".format(name, frame), pmask_*255)
    elif vis==2:
        pmask_ = np.uint8(pmask)
        cv2.imwrite("data/{}/check/{}_{}_pmask.png".format(name, name, frame), pmask_*255)
        cv2.imwrite("data/{}/check/{}_{}_gmask.png".format(name, name, frame), gmask)

    return iou


def compute_convexhull_iou(gt, pr):
    cross_point = compute_cross_point(gt, pr)
    inner_point = compute_inner_point(gt, pr)
    all_inner_point = cross_point + inner_point
    if len(all_inner_point) > 5:
        all_inner_point = np.array(np.reshape(all_inner_point, [int(len(all_inner_point) / 2), 2]), dtype='float32')
        hull_all_inner_point = spatial.ConvexHull(all_inner_point)
        hull_gt = spatial.ConvexHull(gt)
        hull_pr = spatial.ConvexHull(pr)
        convexhull_iou = hull_all_inner_point.area / (hull_gt.area + hull_pr.area - hull_all_inner_point.area)
    else:
        convexhull_iou = 0

    return convexhull_iou


def compute_2d_bb_from_orig_pix(pts, size):
    min_x = np.min(pts[0,:]) / 640.0
    max_x = np.max(pts[0,:]) / 640.0
    min_y = np.min(pts[1,:]) / 480.0
    max_y = np.max(pts[1,:]) / 480.0
    w  = max_x - min_x
    h  = max_y - min_y
    cx = (max_x + min_x) / 2.0
    cy = (max_y + min_y) / 2.0
    new_box = [cx*size, cy*size, w*size, h*size]
    return new_box

def corner_confidences(gt_corners, pr_corners, th=80, sharpness=2, im_width=640, im_height=480):
    ''' gt_corners: Ground-truth 2D projections of the 3D bounding box corners, shape: (16 x nA), type: torch.FloatTensor
        pr_corners: Prediction for the 2D projections of the 3D bounding box corners, shape: (16 x nA), type: torch.FloatTensor
        th        : distance threshold, type: int
        sharpness : sharpness of the exponential that assigns a confidence value to the distance
        -----------
        return    : a torch.FloatTensor of shape (nA,) with 9 confidence values 
    '''
    shape = gt_corners.size()
    nA = shape[1]  
    dist = gt_corners - pr_corners
    num_el = dist.numel()
    num_keypoints = num_el//(nA*2)
    dist = dist.t().contiguous().view(nA, num_keypoints, 2)
    dist[:, :, 0] = dist[:, :, 0] * im_width
    dist[:, :, 1] = dist[:, :, 1] * im_height

    eps = 1e-5
    distthresh = torch.FloatTensor([th]).repeat(nA, num_keypoints) 
    dist = torch.sqrt(torch.sum((dist)**2, dim=2)).squeeze() # nA x 9
    mask = (dist < distthresh).type(torch.FloatTensor)
    conf = torch.exp(sharpness*(1 - dist/distthresh))-1  # mask * (torch.exp(math.log(2) * (1.0 - dist/rrt)) - 1)
    conf0 = torch.exp(sharpness*(1 - torch.zeros(conf.size(0),1))) - 1
    conf = conf / conf0.repeat(1, num_keypoints)
    # conf = 1 - dist/distthresh
    conf = mask * conf  # nA x 9
    mean_conf = torch.mean(conf, dim=1)
    return mean_conf

def corner_confidence(gt_corners, pr_corners, th=80, sharpness=2, im_width=640, im_height=480):
    ''' gt_corners: Ground-truth 2D projections of the 3D bounding box corners, shape: (18,) type: list
        pr_corners: Prediction for the 2D projections of the 3D bounding box corners, shape: (18,), type: list
        th        : distance threshold, type: int
        sharpness : sharpness of the exponential that assigns a confidence value to the distance
        -----------
        return    : a list of shape (9,) with 9 confidence values 
    '''
    dist = torch.FloatTensor(gt_corners) - pr_corners
    num_keypoints = dist.numel()//2
    dist = dist.view(num_keypoints, 2)
    dist[:, 0] = dist[:, 0] * im_width
    dist[:, 1] = dist[:, 1] * im_height
    eps = 1e-5
    dist  = torch.sqrt(torch.sum((dist)**2, dim=1))
    mask  = (dist < th).type(torch.FloatTensor)
    conf  = torch.exp(sharpness * (1.0 - dist/th)) - 1
    conf0 = torch.exp(torch.FloatTensor([sharpness])) - 1 + eps
    conf  = conf / conf0.repeat(num_keypoints, 1)
    conf  = mask * conf 
    return torch.mean(conf)

def sigmoid(x):
    return 1.0/(math.exp(-x)+1.)

def softmax(x):
    x = torch.exp(x - torch.max(x))
    x = x/x.sum()
    return x

def fix_corner_order(corners2D_gt):
    corners2D_gt_corrected = np.zeros((9, 2), dtype='float32')
    corners2D_gt_corrected[0, :] = corners2D_gt[0, :]
    corners2D_gt_corrected[1, :] = corners2D_gt[1, :]
    corners2D_gt_corrected[2, :] = corners2D_gt[3, :]
    corners2D_gt_corrected[3, :] = corners2D_gt[5, :]
    corners2D_gt_corrected[4, :] = corners2D_gt[7, :]
    corners2D_gt_corrected[5, :] = corners2D_gt[2, :]
    corners2D_gt_corrected[6, :] = corners2D_gt[4, :]
    corners2D_gt_corrected[7, :] = corners2D_gt[6, :]
    corners2D_gt_corrected[8, :] = corners2D_gt[8, :]
    return corners2D_gt_corrected

def convert2cpu(gpu_matrix):
    return torch.FloatTensor(gpu_matrix.size()).copy_(gpu_matrix)

def convert2cpu_long(gpu_matrix):
    return torch.LongTensor(gpu_matrix.size()).copy_(gpu_matrix)

def get_region_boxes(output, num_classes, num_keypoints, only_objectness=1, validation=True):
    
    # Parameters
    anchor_dim = 1 
    if output.dim() == 3:
        output = output.unsqueeze(0)
    batch = output.size(0)
    assert(output.size(1) == (2*num_keypoints+1+num_classes)*anchor_dim)
    h = output.size(2)
    w = output.size(3)

    # Activation
    t0 = time.time()
    max_conf = -sys.maxsize
    output    = output.view(batch*anchor_dim, 2*num_keypoints+1+num_classes, h*w).transpose(0,1).contiguous().view(2*num_keypoints+1+num_classes, batch*anchor_dim*h*w)
    grid_x    = torch.linspace(0, w-1, w).repeat(h,1).repeat(batch*anchor_dim, 1, 1).view(batch*anchor_dim*h*w).cuda()
    grid_y    = torch.linspace(0, h-1, h).repeat(w,1).t().repeat(batch*anchor_dim, 1, 1).view(batch*anchor_dim*h*w).cuda()
    
    xs = list()
    ys = list()
    xs.append(torch.sigmoid(output[0]) + grid_x)
    ys.append(torch.sigmoid(output[1]) + grid_y)
    for j in range(1,num_keypoints):
        xs.append(output[2*j + 0] + grid_x)
        ys.append(output[2*j + 1] + grid_y)
    det_confs = torch.sigmoid(output[2*num_keypoints])
    cls_confs = torch.nn.Softmax()(Variable(output[2*num_keypoints+1:2*num_keypoints+1+num_classes].transpose(0,1))).data
    cls_max_confs, cls_max_ids = torch.max(cls_confs, 1)
    cls_max_confs = cls_max_confs.view(-1)
    cls_max_ids   = cls_max_ids.view(-1)
    t1 = time.time()
    
    # GPU to CPU
    sz_hw = h*w
    sz_hwa = sz_hw*anchor_dim
    det_confs = convert2cpu(det_confs)
    cls_max_confs = convert2cpu(cls_max_confs)
    cls_max_ids = convert2cpu_long(cls_max_ids)
    for j in range(num_keypoints):
        xs[j] = convert2cpu(xs[j])
        ys[j] = convert2cpu(ys[j])
    if validation:
        cls_confs = convert2cpu(cls_confs.view(-1, num_classes))
    t2 = time.time()

    # Boxes filter
    for b in range(batch):
        for cy in range(h):
            for cx in range(w):
                for i in range(anchor_dim):
                    ind = b*sz_hwa + i*sz_hw + cy*w + cx
                    det_conf =  det_confs[ind]
                    if only_objectness:
                        conf = det_confs[ind]
                    else:
                        conf = det_confs[ind] * cls_max_confs[ind]
                    
                    if conf > max_conf:
                        max_conf = conf
                        bcx = list()
                        bcy = list()
                        for j in range(num_keypoints):
                            bcx.append(xs[j][ind])
                            bcy.append(ys[j][ind])
                        cls_max_conf = cls_max_confs[ind]
                        cls_max_id = cls_max_ids[ind]
                        box = list()
                        for j in range(num_keypoints):
                            box.append(bcx[j]/w)
                            box.append(bcy[j]/h)
                        box.append(det_conf)
                        box.append(cls_max_conf)
                        box.append(cls_max_id)                        
    t3 = time.time()
    if False:
        print('---------------------------------')
        print('matrix computation : %f' % (t1-t0))
        print('        gpu to cpu : %f' % (t2-t1))
        print('      boxes filter : %f' % (t3-t2))
        print('---------------------------------')
    return box


def read_truths(lab_path, num_keypoints=9):
    num_labels = 2*num_keypoints+3 # +2 for width, height, +1 for class label
    if os.path.getsize(lab_path):
        truths = np.loadtxt(lab_path)
        truths = truths.reshape(truths.size//num_labels, num_labels) # to avoid single truth problem
        return truths
    else:
        return np.array([])

def read_truths_args(lab_path, num_keypoints=9):
    num_labels = 2 * num_keypoints + 1
    truths = read_truths(lab_path)
    new_truths = []
    for i in range(truths.shape[0]):
        for j in range(num_labels):
            new_truths.append(truths[i][j])
    return np.array(new_truths)

def read_pose(lab_path):
    if os.path.getsize(lab_path):
        truths = np.loadtxt(lab_path)
        # truths = truths.reshape(truths.size/21, 21) # to avoid single truth problem
        return truths
    else:
        return np.array([])

def load_class_names(namesfile):
    class_names = []
    with open(namesfile, 'r') as fp:
        lines = fp.readlines()
    for line in lines:
        line = line.rstrip()
        class_names.append(line)
    return class_names

def image2torch(img):
    width = img.width
    height = img.height
    img = torch.ByteTensor(torch.ByteStorage.from_buffer(img.tobytes()))
    img = img.view(height, width, 3).transpose(0,1).transpose(0,2).contiguous()
    img = img.view(1, 3, height, width)
    img = img.float().div(255.0)
    return img

def read_data_cfg(datacfg):
    options = dict()
    options['gpus'] = '0'
    options['num_workers'] = '10'
    with open(datacfg, 'r') as fp:
        lines = fp.readlines()

    for line in lines:
        line = line.strip()
        if line == '':
            continue
        key,value = line.split('=')
        key = key.strip()
        value = value.strip()
        options[key] = value
    return options

def scale_bboxes(bboxes, width, height):
    import copy
    dets = copy.deepcopy(bboxes)
    for i in range(len(dets)):
        dets[i][0] = dets[i][0] * width
        dets[i][1] = dets[i][1] * height
        dets[i][2] = dets[i][2] * width
        dets[i][3] = dets[i][3] * height
    return dets
      
def file_lines(thefilepath):
    count = 0
    thefile = open(thefilepath, 'rb')
    while True:
        buffer = thefile.read(8192*1024)
        if not buffer:
            break
        count += buffer.count(b'\n')
    thefile.close( )
    return count

def get_image_size(fname):
    '''Determine the image type of fhandle and return its size.
    from draco'''
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24: 
            return
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg' or imghdr.what(fname) == 'jpg':
            try:
                fhandle.seek(0) # Read 0xff next
                size = 2 
                ftype = 0 
                while not 0xc0 <= ftype <= 0xcf:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2 
                # We are at a SOFn block
                fhandle.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception: #IGNORE:W0703
                return
        else:
            return
        return width, height

def logging(message):
    print('%s %s' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), message))

def read_pose(lab_path):
    if os.path.getsize(lab_path):
        truths = np.loadtxt(lab_path)
        return truths
    else:
        return np.array([])
