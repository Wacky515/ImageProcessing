# !/usr/bin/python
# -*- coding: utf-8 -*-
# --------------------------------------------------# {{{
# file_name:   tplmatching
# Purpose:     TemplateMatching
#
# Author:      Kilo11
#
# Created:     23/03/2016
# Copyright:   (c) SkyDog 2016
# Licence:     SDS10001.200
# --------------------------------------------------
u""" �e���v���[�g�}�b�`���O�ɂ��摜���� """
# }}}

# TODO: Python3�n �Ή��I�I�I
# TODO: �֐����͓����ɂ���
# TODO: �ϐ��� "[��敪]_[���敪]"
# TODO: Unicode�������e������ " u"body" " -> " "body" " �ɕύX
# DONE: ������̖����� % �`������ format �`���ɕύX
# DONE: "print" -> "print()" �ɕύX

# ���W���[�� �C���|�[�g# {{{
import numpy as np
import os
# import glob
import time
# import unittest

import cv2
# import cv2.cv as cv

import trim as tm

import sys
sys.path.append("D:\OneDrive\Biz\Python\SaveDate")

import savedata as sd

# sys���W���[�� �����[�h
reload(sys)

# �f�t�H���g�̕����R�[�h �o��
sys.setdefaultencoding("utf-8")
# }}}


def terminate(name_cap=0, time_wait=33):
    u""" �o�͉摜 �I������ """# {{{
    # name_cap: 0: �Î~�� 1: ����
    cv2.waitKey(time_wait)
    if name_cap != 0:
        name_cap.release
    cv2.destroyAllWindows()
    print("Terminated...")
    sys.exit()
# }}}


class GetImage:
    u""" �摜�E���� �擾�N���X """
    def __init__(self, image):
        self.image = image

    def get_image(self, conversion=1):
        u""" �摜�E���� �Ǎ��� """
        try:
            image = cv2.imread(self.image, conversion)
            return image
        # �摜�擾 �G���[����
        except:
            print ("Image data is not found...")
            return False

    def display(self, name_window, image, _type=1):
        u""" �摜�E���� ��ʏo�� """
        # _type: 0: �Î~�� 1: ���� �؊���
        # �Î~�斳�����莞 ���� �� "is None" �ɂ��� ����m�F�I�I�I
        if image is None and _type == 0:
            print ("Getting image...")
            image = self.get_image()
        print ("Display {}s...".format(name_window))
        cv2.namedWindow(name_window, cv2.WINDOW_AUTOSIZE)
        cv2.imshow(name_window, image)
        print (u"�摜�̑傫�����擾���鏈���������I�I�I")
        if _type == 0:
            # �Î~��̏o�͕ێ�����
            terminate(0, 0)


class ConvertImage(GetImage):
    u""" �摜�E���� �ϊ��N���X """  # {{{
    def __init__(self):
        pass

    def grayscale(self, image):
        u""" �O���[�X�P�[�� �ϊ����� """
        print ("Convert grayscale...")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return gray

    def adaptive_threashold(self, image):
        u""" �K���I��l�� �ϊ����� """
        gray = self.grayscale(image)
        # �K���I��l��(Adaptive Gaussian Thresholding) �p�����^��`# {{{
        # *** �K���I��l�� ��� ***
        # 1��f���ɁA�C�ӂ̋ߖT��f����ʂ�臒l���Z�o
        # *** �ȏ� ***
        # }}} """
        # �ő�臒l
        thresh_max = 255
        # 臒l�Z�o�A���S���Y��# {{{
        # GaussianC:�C�ӂ̋ߖT��f��Gaussian�ɂ��d�t���i�ߖT���d���j�ő��a��
        # 臒l���Z�o
        # MeanC:�C�ӂ̋ߖT��f���Z�p���ς�臒l���Z�o
        # }}} """
        algo = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
        # algo = cv2.ADAPTIVE_THRESH_MEAN_C
# 臒l����
        thresh_type = cv2.THRESH_BINARY
        # thresh_type = cv2.THRESH_BINARY_INV
        # �؎�鐳���`�̈�̉�f���i3�A5�A7... ��̂݁I�j
        area_calc = 7
        # ���Z�萔# {{{
        #   ���͂������F�̎��A���Z����臒l���Ӑ}�I�ɓˏo����
        #   �w�i�̈�̃m�C�Y�E�F��炬�̉e����ጸ����
        # }}}
        subtract = 4
        # �K���I��l�� �ϊ�����
        print ("Convert adaptive threashold...")
        cat = cv2.adaptiveThreshold
        adpth = cat(gray, thresh_max, algo, thresh_type, area_calc, subtract)
        return adpth

    def bilateral_filter(self, image):
        u""" �o�C���e�����t�B���^ ���� """
        gray = self.grayscale(image)
        # �؎�鐳���`�̈�̉�f���i3�A5�A7... ��̂݁I�j
        # ���l���傫���قǂڂ₯��
        area_calc = 7
        # �F��Ԃɂ�����t�B���^�V�O�}      �傫���Ȃ�ƐF�̗̈悪���傫���Ȃ�
        color_sigma = 12
        # ���W��Ԃɂ�����t�B���^�V�O�}    �傫���Ȃ�Ƃ�艓���̉�f���m���e������
        metric_sigma = 3
        print ("Bilateral filtering...")
        cvf = cv2.bilateralFilter
        blr = cvf(gray, area_calc, color_sigma, metric_sigma)
        return blr

    def discriminantanalyse(self, image):
        u""" ���ʕ��͖@ ���� """
        image = self.bilateral_filter(image)
        thresh_std = 40
        thresh_max = 255
        method = cv2.THRESH_BINARY + cv2.THRESH_OTSU
        print ("Discriminant analysing...")
        cth = cv2.threshold
        ret, dcta = cth(image, thresh_std, thresh_max, method)
        return dcta

    def binarize(self, image):
        u""" ��l�� ���� """
        image = self.bilateral_filter(image)
        thresh_std = 70
        thresh_max = 255
        method = cv2.THRESH_BINARY_INV
        print ("Binarizing...")
        cth = cv2.threshold
        ret, binz = cth(image, thresh_std, thresh_max, method)
        return binz

    def normalize(self, image):
        u""" ���K�� ���� """
        # alpha�Abeta ����i�킩���I�I�I�j# {{{
        # alpha:�m�������K���̏ꍇ�A���K�������m�����l�B�͈͐��K���̏ꍇ�A���E
        # beta:�m�������K���̏ꍇ�A�s�g�p�B�͈͐��K���̏ꍇ�A�̏�E
        # }}}
        alpha = 0
        beta = 1
        algo = cv2.NORM_MINMAX
        print ("Normalizing...")
        norm = cv2.normalize(image, alpha, beta, algo)
        return norm
# }}}


class Tplmatching:
    u""" �e���v���[�g�}�b�`���O �N���X """
    def __init__(self):
        pass

    def tplmatch(self, image, tpl):
        u""" �e���v���[�g�}�b�`���O ���� """
        # �ގ�����A���S���Y�� ���# {{{
        # CV_TM_SQDIFF    :�P�x�l�̍��̂Q��̍��v     �������قǗގ�
        # CV_TM_CCORR     :�P�x�l�̑���               �傫���قǗގ�
        # CV_TM_CCOEFF    :�P�x�l�̕��ς�����������   �傫���قǗގ�
        #                 �i�e���v���[�g�摜�ƒT���摜�̖��邳�ɍ��E����ɂ����j
        # }}} """
        algo = cv2.TM_CCOEFF_NORMED
        match = cv2.matchTemplate(image, tpl, algo)
        # �ގ��x�̍ŏ��E�ő�l�Ɗe���W �擾
        value_min, value_max, loc_min, loc_max = cv2.minMaxLoc(match)
        return match, value_min, value_max, loc_min, loc_max


class ImageProcessing:
    u""" ����擾 �N���X """
    def __init__(self):
        self.ci = ConvertImage()
        self.tm = Tplmatching()
        # ���� �擾
        self.cap = cv2.VideoCapture(0)

    def init_get_camera_image(self, name):
        u""" �J�������瓮��擾 """
        # �J�����L���v�`�����̃C�j�V�����C�Y �f�B���C����
        time.sleep(0.1)
        if not self.cap.isOpened():
            print ("Can not connect camera...")
            terminate()
            # �g���b�N�o�[ ��`(�ł��Ȃ�)�I�I�I# {{{
            #        name_bar = "Max threshold"
            #        print (thresh_max)
            # # �g���b�N�o�[ ����
            #        def set_parameter(value):
            #            thresh_max = cv2.getTrackbarPos(name_bar, name_window)
            #            thresh_max = cv2.setTrackbarPos(name_bar, name_window)
            #        cv2.createTrackbar(name_bar, name_window,
            #           0, 255, self.thresh_max)
            #        name_window = "Adaptive Threashold cap"
            # }}}
        cv2.namedWindow(name, cv2.WINDOW_AUTOSIZE)

    def run(self, name, search, extension=".png", dir_master="MasterImage"):
        u""" ����擾 �����i���C�����[�`���j """  # {{{
        print ("-------------------------------------------------")
        print ("Start template matching")
        print ("-------------------------------------------------")
        print ("\t*** Search master mode ***\r\n")
        cwd = os.getcwd()
        path_master = cwd + "\\" + dir_master
        print ("Master directory: \r\n\t" + path_master)

        # �}�X�^�[�摜 ����
        sda = sd.SaveData(search, path_master)
        set_name, name_master, match_flag = sda.get_name_max(extension)
        print ("\t*** Return search master mode ***\r\n")

        # �}�X�^�[�摜�L�� ����
        if match_flag is False:
            print ("No match master")
            print ("Go get master mode(no match master case)\r\n")
            self.get_master(search, extension, path_master)
            set_name, name_master, match_flag = sda.get_name_max(extension)
            print ("Get master name: " + str(name_master))
        else:
            print ("Match master name: " + str(name_master))
            print ("Match master extension: " + str(extension))

        self.init_get_camera_image(name)

        # !!!: ��������
        count = 0
        while True:
            if count < 1:
                print ("Initial delay")
                time.sleep(0.1)
            get_flag, frame = self.cap.read()

            if self.check_get_flag(get_flag) is False:
                break
            if self.check_get_frame(frame) is False:
                continue

            # TODO: ������� �\���I�I�I
            cv2.imshow(name, frame)
            print ("Capture is running...")
            count += 1
        # !!!: �ȏ�܂ł�class�ɂ�������"while"����"frame"��
        # "while"�O�ɏo���Ȃ��̂Œf�O�I�I�I
        # ���֐��ɂ���(�ł��Ȃ������I�I�I)�H�H�H
            # }}}

            # ���� �ϊ��E�摜�����i�܂Ƃ߂�j�I�I�I# {{{
            adpth = self.ci.adaptive_threashold(frame)
            self.ci.display("Adaptive threashold", adpth, 1)
            dcta = self.ci.discriminantanalyse(frame)
            self.ci.display("Discriminant analyse", dcta, 1)
            binz = self.ci.binarize(frame)
            self.ci.display("Bilateral filter", binz, 1)
# }}}

            # �e���v���[�g�}�b�`���O ����
            print("\r\nMaster name: " + str(name_master) + str(extension) + "\r\n")
            master = str(path_master) + ".\\"\
                    + str(name_master) + str(extension)
            master = cv2.imread(str(master), cv2.IMREAD_COLOR)
            self.ci.display("Master", master)

            match, value_min, value_max, loc_min, loc_max \
                    = self.tm.tplmatch(frame, master)
            print (value_max)

            # 2016/06/03 �����܂ŁI�I�I
            # "t"�L�[���� �}�X�^�[�摜�擾���[�h �J��
            if cv2.waitKey(33) == ord("t"):
                print "\r\nInput key \"t\""
                print("Go get master mode\r\r\n")
                time.sleep(1)
                self.get_master(search, extension, path_master)
                set_name, name_master, match_flag = sda.get_name_max(extension)
                print ("Get master name: " + str(name_master))
                # img = "master_source{}".format(extension)
                # cv2.imwrite(img, frame)
                # trim = tm.Trim(img, search, extension, path_master)
                # trim.trim()

            # ���̏I�������I�I�I
            # "q"�L�[���� �I������
            if cv2.waitKey(33) == ord("e"):
                print "\r\nInput key \"e\""
                time.sleep(1)
                print ("*** End process ***\t\r\n")
                break
            # if cv2.waitKey(33) > 0:
            #     break
            #     # terminate(cap)


    def get_master(self, search, extension, path):
        u""" �}�X�^�[�摜 �Ǎ��� """
        print ("*** Start get master mode ***\t")
        print ("Search master name: " + str(search))
        name = "Get master image"
        text2 = "Quit: Long press \"q\" key"
        text3 = "Trim mode: Long press \"t\" key"

        print ("Master image name: " + str(search))

        self.init_get_camera_image(name)

        count = 0
        while True:
            if count < 1:
                print ("Initial delay")
                time.sleep(0.1)
            get_flag, frame = self.cap.read()
            get_flag_draw, frame_draw = self.cap.read()

            if self.check_get_flag(get_flag) is False:
                break
            if self.check_get_frame(frame) is False:
                continue

            # ������@������ �\���ʒu �擾
            text_offset = 10
            baseline = frame.shape[0] - text_offset
            origin = 1, baseline

            # ������@������ �\��
            trim = tm.Trim(frame_draw, search, extension, path, 1)
            text_height = trim.write_text(text2, origin)
            trim.write_text(text3,\
                    (origin[0], origin[1] - text_offset - text_height[1]))

            cv2.imshow(name, frame_draw)
            print ("Master captcha")
            count += 1

            # "t"�L�[���� �}�X�^�[�摜�擾���[�h �J��
            if cv2.waitKey(33) == ord("t"):
                print "\r\nInput key \"t\""
                print("Go master mode")
                time.sleep(1)
                img = "master_source{}".format(extension)
                cv2.imwrite(img, frame)
                trim = tm.Trim(img, search, extension, path)
                trim.trim()

            # "q"�L�[���� �I������
            if cv2.waitKey(33) == ord("q"):
                print "\r\nInput key \"q\""
                time.sleep(1)
                print ("*** End get master mode ***\t\r\n")
                break

    def check_get_flag(self, flag):
        u""" ����擾�~�X�� �X�L�b�v���� """  # {{{
        if flag is False:
            print ("Can not get end flag")
            return False
            # }}}

    def check_get_frame(self, frame):
        u""" ���[�v �I������ """  # {{{
        if frame is None:
            print ("Can not get video frame")
            return False
            # }}}


def main():
    # vim�e�X�g�p�e�ϐ� ��`# {{{
    # �e�X�g�o��
    print ("\r\n--------------------------------------------------")
    print ("Information")
    print ("--------------------------------------------------")
    print ("Default current directory is...")
    print ("\t" + os.getcwd())
    print ("\r\nAnd then...")
    os.chdir("D:\OneDrive\Biz\Python\ImageProcessing")
    print ("\t" + os.getcwd())
    print (u"\r\n��������������������������������������������������")
    print ("Start main")
    print (u"��������������������������������������������������")
    import pdb; pdb.set_trace()

    path = "D:\\OneDrive\\Biz\\Python\\ImageProcessing"
    smpl_pic = "D:\\OneDrive\\Biz\\Python\\ImageProcessing\\tpl_1.png"
    smpl_pic2 = "D:\\OneDrive\\Biz\\Python\\ImageProcessing\\tpl_2.png"
# }}}

    # �e���v���[�g�}�b�`���O �e�X�g# {{{
    cip = ImageProcessing()
    cip.run("Raw capture", "masterImage")
    # print ("Movie captcha end...")
    # }}}

#     # �Î~��擾 �e�X�g# {{{
#     gim = GetImage(smpl_pic)
#     gim2 = GetImage("tpl_3.png")
#     # gim.diplay("Tes1", 0, 0)
#     gim2.display("Tes2", 0, 0)
#     print ("Main loop end...")
# # }}}

# # ����擾 �e�X�g# {{{
#     cav = CapVideo()
#     cav.get_video("Capture_test")
#     frame_test = cav.frame
#     if frame_test is None:
#         gm = GetImage(smpl_pic)
#         gm.get_image()
#     name = "Test"
#     Image = cv2.imread(smpl_pic2)
#     cv2.namedWindow(name, cv2.WINDOW_AUTOSIZE)
#     cv2.imshow(name, Image)
#     cv2.imshow(name, frame_test)
#     # ���̏o�͕ێ������I�I�I
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#
#     image = cv2.imread("tpl_2.png")
#     ci = ConvertImage()
#     ci.adaptive_threashold(image, "Adaptive Threashold", 0)
#     print ("Sudah cap")
# # }}}

    # # �h�L�������g�X�g�����O# {{{
    # print (GetImage.__doc__)
    # print (help(__name__))
    # }}}

if __name__ == '__main__':
    main()

#    unittest.main()