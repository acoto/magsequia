from subprocess import Popen, PIPE
import os


def run_command(args):
    p = Popen(args, stdout=PIPE, stderr=PIPE)
    p.communicate()
    if p.returncode == 0:
        return True
    else:
        print("Error in {}".format(args[0]))
        return False


def main(settings, project):
    file_array = ["201901", "201902", "201903", "201904", "201905", "201906", "201907", "201908"]
    db=settings["mysql.host"]
    user=settings["mysql.user"]
    pwd=settings["mysql.password"]
    outDir = settings["repository.path"] +"/maps/"+project+"/"
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    #file_array = ["201901"]
    for a_file in file_array:
        print(a_file)
        args = [
            "goblet-resetaggregate",
            "-H %s" %db,
            "-u %s"%user,
            "-p %s"%pwd,
            "-d ndvibioversity",
            "-s shapeDistritos",
            "-c",
        ]
        if run_command(args):
            args = [
                "goblet-aggregatedataset",
                "-H %s" %db,
                "-u %s"%user,
                "-p %s"%pwd,
                "-d ndvibioversity",
                "-s shapeDistritos",
                "-t sensidistrito",
            ]
            if run_command(args):
                args = [
                    "goblet-classifyaggregate",
                    "-H %s" %db,
                    "-u %s"%user,
                    "-p %s"%pwd,
                    "-d ndvibioversity",
                    "-s shapeDistritos",
                    "-t sensidistrito",
                    "-c 10:0 1,20:1 2,30:2 3"
                ]
                if run_command(args):
                    if not os.path.exists(outDir+"./sensitivity-distrito.shp"):
                        args = [
                            "goblet-outputshape",
                            "-H %s" %db,
                            "-u %s"%user,
                            "-p %s"%pwd,
                            "-d ndvibioversity",
                            "-s shapeDistritos",
                            "-t sensidistrito",
                            "-i c",
                            "-o "+outDir+"./sensitivity-distrito.shp"
                        ]
                        run_command(args)
                    args = [
                        "goblet-aggregatedataset",
                        "-H %s" %db,
                        "-u %s"%user,
                        "-p %s"%pwd,
                        "-d ndvibioversity",
                        "-s shapeDistritos",
                        "-t ndvi" + a_file,
                    ]
                    if run_command(args):
                        args = [
                            "goblet-classifyaggregate",
                            "-H %s" %db,
                            "-u %s"%user,
                            "-p %s"%pwd,
                            "-d ndvibioversity",
                            "-s shapeDistritos",
                            "-t ndvi" + a_file,
                            "-c 1:0 4375,2:4375 5000,3:5000 5625,4:5625 10000",
                        ]
                        if run_command(args):
                            args = [
                                "goblet-outputshape",
                                "-H %s" %db,
                                "-u %s"%user,
                                "-p %s"%pwd,
                                "-d ndvibioversity",
                                "-s shapeDistritos",
                                "-t ndvi" + a_file,
                                "-i c",
                                "-o "+outDir+"./hazard-distrito-" + a_file + ".shp",
                            ]
                            if run_command(args):
                                args = [
                                    "goblet-combineaggregate",
                                    "-H %s" %db,
                                    "-u %s"%user,
                                    "-p %s"%pwd,
                                    "-d ndvibioversity",
                                    "-s shapeDistritos",
                                ]
                                if run_command(args):
                                    args = [
                                        "goblet-outputshape",
                                        "-H %s" %db,
                                        "-u %s"%user,
                                        "-p %s"%pwd,
                                        "-d ndvibioversity",
                                        "-s shapeDistritos",
                                        "-i b",
                                        "-o "+outDir+"./vulnerability-distrito-" + a_file + ".shp",
                                    ]
                                    run_command(args)


