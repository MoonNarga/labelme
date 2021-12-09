import os
import json
import shutil

class dataProcess():

    def utf2gbk(self, path):
        for root, dirs, files in os.walk(path):
            for f in files:
                if (f[-4:] == "json"):
                    fp = open(os.path.join(root, f), 'r', encoding="utf-8")
                    content = json.load(fp)
                    fp = open(os.path.join(root, f), 'w', encoding="gbk")
                    json.dump(content, fp, indent=2, ensure_ascii=False)

    def json2dataset(self, path):
        for root, dirs, files in os.walk(path):
            for f in files:
                if (f[-4:] == "json"):
                    os.system("labelme_json_to_dataset \"" + os.path.join(root, f) + "\"" + " -o \"" + os.path.join(root, f[:-5]) + "\"")
                    # print("labelme_json_to_dataset \"" + os.path.join(root, f) + "\"" + " -o \"" + os.path.join(root, f[:-5]) + "\"")

    def img_cp(self, path, pathdir, root):
        for root, dirs, files in os.walk(path):
            for di in dirs:
                if (di != root):
                    shutil.copy(os.path.join(root, di, "img.png"), os.path.join(pathdir, di + ".png"))
                    
    def json2txt(self, path):
        for root, dirs, files in os.walk(path):
            for f in files:
                if (f[-4:] == "json"):
                    fp = open(os.path.join(root, f), 'r', encoding="gbk")
                    content = json.load(fp)
                    fp = open(os.path.join(root, f[:-5] + ".txt"), 'w', encoding='utf-8')
                    for shape in content["shapes"]:
                        points = shape["points"]
                        x_center = (points[1][0] + points[0][0]) / 2 / content["imageWidth"]
                        y_center = (points[1][1] + points[0][1]) / 2 / content["imageHeight"]
                        w_per = (points[1][0] - points[0][0]) / content["imageWidth"]
                        h_per = (points[1][1] - points[0][1]) / content["imageHeight"]
                        file_str = "0 " + str(round(x_center, 6)) + ' ' + str(round(y_center, 6)) + ' ' + str(round(w_per, 6)) + ' ' + str(round(h_per, 6))
                        fp.write(file_str + '\n')
                    
    def createImageInfo(self, srcDic, dstFile, mode):
        for root, dirs, files in os.walk(srcDic):
            fp = open(dstFile, 'w', encoding='utf-8')
            for f in files:
                fp.write("./images/" + mode + '/' + f + '\n')

if __name__ == '__main__':
    path = "C:/Users/MoonN/Desktop/oldLabelSet/iodine/images/train"
    pathdir = "C:/Users/MoonN/Desktop/n"
    dataP = dataProcess()
    # dataP.json2dataset(path)
    dataP.img_cp(path, pathdir, "train")