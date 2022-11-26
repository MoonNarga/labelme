import os
import json
import shutil
import random


class dataProcess():

    def __init__(self, path: str) -> None:
        self.category = self.load_category(path)

    # 读取path中的labels.txt文件，获取类别dict
    def load_category(self, path: str) -> dict:
        res = {}
        cnt = -1
        for line in open(os.path.join(path, "labels.txt"), "r", encoding="utf-8"):
            res[line[:-1]] = str(cnt)
            cnt += 1
        print(res)
        return res

    def utf2gbk(self, path):
        for root, dirs, files in os.walk(path):
            for f in files:
                if (f[-4:] == "json"):
                    fp = open(os.path.join(root, f), 'r', encoding="utf-8")
                    content = json.load(fp)
                    fp = open(os.path.join(root, f), 'w', encoding="gbk")
                    json.dump(content, fp, indent=2, ensure_ascii=False)

    def gbk2utf(self, path):
        for root, dirs, files in os.walk(path):
            for f in files:
                if (f[-4:] == "json"):
                    fp = open(os.path.join(root, f), 'r', encoding="gbk")
                    content = json.load(fp)
                    fp = open(os.path.join(root, f), 'w', encoding="utf-8")
                    json.dump(content, fp, indent=2, ensure_ascii=False)

    # 自动生成dataset
    def json2dataset(self, path):
        for root, dirs, files in os.walk(path):
            for f in files:
                if (f[-4:] == "json"):
                    os.system("labelme_json_to_dataset \"" + os.path.join(root,
                              f) + "\"" + " -o \"" + os.path.join(root, f[:-5]) + "\"")
                    # print("labelme_json_to_dataset \"" + os.path.join(root, f) + "\"" + " -o \"" + os.path.join(root, f[:-5]) + "\"")

    def img_cp(self, src, dst):
        for root, dirs, files in os.walk(src):
            for di in dirs:
                if (di != root):
                    shutil.copy(os.path.join(root, di, "img.png"),
                                os.path.join(dst, di + ".png"))

    # 生成yolo格式txt文件
    def json2txt(self, src: str, dst: str, encoding: str):
        for root, dirs, files in os.walk(src):
            for f in files:
                if (f[-4:] == "json"):
                    fp = open(os.path.join(root, f), 'r', encoding=encoding)
                    content = json.load(fp)
                    fp = open(os.path.join(
                        dst, f[:-5] + ".txt"), 'w', encoding='utf-8')
                    for shape in content["shapes"]:
                        label = shape["label"]
                        points = shape["points"]
                        xMin, yMin, xMax, yMax = points[0][0], points[0][1], points[1][0], points[1][1]
                        for point in points:
                            xMin = min(xMin, point[0])
                            yMin = min(yMin, point[1])
                            xMax = max(xMax, point[0])
                            yMax = max(yMax, point[1])
                        x_center = (xMin + xMax) / 2 / content["imageWidth"]
                        y_center = (yMin + yMax) / 2 / content["imageHeight"]
                        w_per = (xMax - xMin) / \
                            content["imageWidth"]
                        h_per = (yMax - yMin) / \
                            content["imageHeight"]
                        file_str = self.category[label] + ' ' + str(round(x_center, 6)) + ' ' + str(
                            round(y_center, 6)) + ' ' + str(round(w_per, 6)) + ' ' + str(round(h_per, 6))
                        fp.write(file_str + '\n')

    def createRandomImageInfo(self, src: str, dst: str):
        for root, dirs, files in os.walk(src):
            random.shuffle(files)
            length = len(files)
            train = int(0.8 * length)
            test = int(0.1 * length)
            fp = open(os.path.join(dst, "train.txt"), 'w', encoding='utf-8')
            for f in files[:train]:
                fp.write("./images/" + f + '\n')
            fp = open(os.path.join(dst, "test.txt"), 'w', encoding='utf-8')
            for f in files[train:train + test]:
                fp.write("./images/" + f + '\n')
            fp = open(os.path.join(dst, "val.txt"), 'w', encoding='utf-8')
            for f in files[train + test:]:
                fp.write("./images/" + f + '\n')


def main():
    dataP = dataProcess("/home/moonnarga/workspace/datasets/StateGrid")

    src = "/home/moonnarga/workspace/datasets/StateGrid/data_ann"
    dst = "/home/moonnarga/workspace/datasets/StateGrid/labels"
    # dataP.gbk2utf(path)
    # dataP.json2dataset(path)
    # dataP.img_cp(
    #     "/home/moonnarga/workspace/datasets/StateGrid/data_annotated", dst)
    # dataP.json2txt(src, dst, "utf-8")
    # dataP.createRandomImageInfo(src, dst)


if __name__ == '__main__':
    main()
