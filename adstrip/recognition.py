##
# Frame recognition engine
# @author Patrick Kage

import cv2
import numpy as np
import logging
import math
from skimage.measure import compare_ssim

class TemplateRecognizer:

    def fit(self, subj, max_img):
        # load the template
        ho, wo = max_img.shape
        h, w = subj.shape

        # scale the pattern down if it's too large
        if w > wo or h > ho:
            # scale factor (height-based)
            scale_factor = ho / h
            # check if it's not gonna be too wide
            if wo/w < scale_factor:
                scale_factor = wo/w

            # perform the resize
            subj = cv2.resize(subj, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_AREA)

            # hold on to the resizer
            h, w = subj.shape

        return h, w, subj

    def fill_crop(self, subj, max_img):
        # load the template
        ho, wo = max_img.shape
        h, w = subj.shape

        # scale factor (height-based)
        scale_factor = ho / h
        # check if it's not gonna stick off the end
        if w*scale_factor < wo:
            scale_factor = wo / w

        # perform the resize
        subj = cv2.resize(subj, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_AREA)

        # crop
        subj = subj[:ho, :wo]

        return subj


    def test(self, frame, templ):
        from matplotlib import pyplot as plt
        logging.debug('starting template find');
        img = cv2.imread(frame,0)
        print(img);

        # look in lower right third (almost)
        ho, wo = img.shape
        ho = math.floor(ho * 0.66);
        wo = math.floor(wo * 0.66);
        img = img[ho:, wo:]

        # make a copy so we can use it later
        img2 = img.copy()

        # load the template
        template = cv2.imread(templ,0)
        h, w, template = self.fit(template, img)

        # invert image
        template = np.full_like(template, 255) - template
        _, template = cv2.threshold(template, 127, 255, cv2.THRESH_BINARY)

        # All the 6 methods for comparison in a list
        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                    'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

        plots = []
        for meth in methods:
            img = img2.copy()
            method = eval(meth)

            # Apply template Matching
            res = cv2.matchTemplate(img,template,method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = min_loc
            else:
                top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)

            cv2.rectangle(img,top_left, bottom_right, 255, 2)
            crop = img[top_left[1]:top_left[1] + h, top_left[0]:top_left[0] + w]
            _, crop = cv2.threshold(crop, 127, 255, cv2.THRESH_BINARY)

            score, diff = compare_ssim(self.fill_crop(template,crop), crop, full=True)

            plots.append( (res.copy(), img.copy(), crop, meth, diff, score) )


        f, axarr = plt.subplots(len(plots), 6)
        for i in range(0, len(plots)):
            axarr[i, 0].text(0,0.5, '{}\n{}'.format(plots[i][3],plots[i][5]))
            axarr[i, 0].axis('off')
            axarr[i, 1].imshow(plots[i][0], cmap='gray')
            axarr[i, 1].axis('off')
            axarr[i, 2].imshow(plots[i][1], cmap='gray')
            axarr[i, 2].axis('off')
            axarr[i, 3].imshow(plots[i][2], cmap='gray')
            axarr[i, 3].axis('off')
            axarr[i, 4].imshow(template, cmap='gray')
            axarr[i, 4].axis('off')
            axarr[i, 5].imshow(plots[i][4], cmap='gray')
            axarr[i, 5].axis('off')

        plt.tight_layout()
        f.subplots_adjust(hspace=0.03)

        plt.show()

    def detect(self, frame, templ):
        logging.debug('starting template find with {}'.format(templ));
        img = cv2.imread(frame,0)

        # look in lower right third (almost)
        ho, wo = img.shape
        ho = math.floor(ho * 0.66);
        wo = math.floor(wo * 0.66);
        img = img[ho:, wo:]

        # load the template
        template = cv2.imread(templ,0)
        h, w, template = self.fit(template, img)

        # threshold the template
        _, template = cv2.threshold(template, 127, 255, cv2.THRESH_BINARY)

        # Apply template matching
        res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)

        # figure out where the result sits
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        # create & threshold the crop
        crop = img[top_left[1]:top_left[1] + h, top_left[0]:top_left[0] + w]
        _, crop = cv2.threshold(crop, 127, 255, cv2.THRESH_BINARY)

        # make a score
        score, diff = compare_ssim(self.fill_crop(template,crop), crop, full=True)

        return score;
