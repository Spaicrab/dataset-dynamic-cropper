"""Bounding boxes util"""

class BoundingBoxes:
    """A representation of multiple bounding boxes for Yolo Format"""
    def __init__(self, label, format="normalized"):
        self.format = format
        self.bbs = []
        for line in label:
            bb = line.split()
            for i in range(1, len(bb)):
                if self.is_normalized(): bb[i] = float(bb[i])
                else: bb[i] = int(bb[i])
            self.bbs.append(bb)
        if self.bbs == []:
            raise Exception("Label file is empty.")
    
    def is_normalized(self):
        """Returns True if this instance is in normalized format, otherwise False"""
        format = self.format.lower()
        if format == "normalized": return True
        elif format == "pixel": return False
        else:
            txt = "{format} format doesn't exist. Choose between Normalized and Pixel".format(format = format)
            raise Exception(txt)
        return

    def bb_values(self, i):
        """Returns the values of this instance's bounding box with index i"""
        bb = self.bbs[i]
        bb_class = bb[0]
        bb_x = bb[1]
        bb_y = bb[2]
        bb_w = bb[3]
        bb_h = bb[4]
        return bb_class, bb_x, bb_y, bb_w, bb_h

    def bb_label(self, i) -> str:
        """Returns the label of this instance's bounding box with index i"""
        bb = self.bbs[i]
        bb_label = str(bb[0])
        for j in range(1, len(bb)):
            bb_label += " " + str(bb[j])
        return bb_label

    def label(self) -> str:
        """Returns this instance's label"""
        label = self.bb_label(0)
        for i in range(1, len(self.bbs)):
            label += "\n" + self.bb_label(i)
        return label

    def normalize(self, img_w, img_h):
        """Converts this instance to normalized format"""
        if self.is_normalized: raise Exception("Bounding boxes are already normalized.")
        self.format = "normalized"
        for i in range(len(self.bbs)):
            bb = self.bbs[i]
            bb[1] = float(bb[1] / img_w)
            bb[2] = float(bb[2] / img_h)
            bb[3] = float(bb[3] / img_w)
            bb[4] = float(bb[4] / img_h)
            self.bbs[i] = bb

    def to_pixel(self, img_w, img_h):
        """Converts this instance to pixel format"""
        if not self.is_normalized: raise Exception("Bounding boxes are already in pixel format.")
        self.format = "pixel"
        for i in range(len(self.bbs)):
            bb = self.bbs[i]
            bb[1] = int(bb[1] * img_w)
            bb[2] = int(bb[2] * img_h)
            bb[3] = int(bb[3] * img_w)
            bb[4] = int(bb[4] * img_h)
            self.bbs[i] = bb

    def borders(self):
        """Returns this instance's borders (Leftmost, Rightmost, Bottom, Top)"""
        bb_class, bb_x, bb_y, bb_w, bb_h = self.bb_values(0)
        xM = bb_x + bb_w / 2
        xm = bb_x - bb_w / 2
        yM = bb_y + bb_h / 2
        ym = bb_y - bb_h / 2
        for i in range(1, len(self.bbs)):
            bb_class, bb_x, bb_y, bb_w, bb_h = bbs.bb_values(i)
            xM = max(xM, bb_x + bb_w / 2)
            xm = min(xm, bb_x - bb_w / 2)
            yM = max(yM, bb_y + bb_h / 2)
            ym = min(ym, bb_y - bb_h / 2)
        return xM, xm, yM, ym

    def to_cropped(self, cropped_img_w, cropped_img_h, center_x, center_y):
        """Converts this instance to a cropped version of itself"""
        if not self.is_normalized: raise Exception("Bounding boxes need to be in pixel format.")
        self.format = "normalized"
        offset_x = center_x - cropped_img_w / 2
        offset_y = center_y - cropped_img_h / 2
        for i in range(len(self.bbs)):
            bb = self.bbs[i]
            for j in range(1, len(bb)): bb[j] = float(bb[j])
            bb[1] = float((bb[1] - offset_x) / cropped_img_w)
            bb[2] = float((bb[2] - offset_y) / cropped_img_h)
            bb[3] = float(bb[3] / cropped_img_w)
            bb[4] = float(bb[4] / cropped_img_h)
            self.bbs[i] = bb
        