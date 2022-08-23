#!/usr/bin/env python

mail_body_list = ['2022-08-23_14-16-21<br>Hi, \r\nI stopped doing Go to kitchen because of timeout.\r\nI failed to upload the following data:\r\n    trashcan_inside.jpg\r\n\r\ngo_to_kitchen_result.yaml: https://drive.google.com/uc?id=1Mo9UVSaDZRbO37tkF9TIBwiQXYkETQHe \r\ngo_to_kitchen_head_camera.mp4: https://drive.google.com/uc?id=1aXBM7ROdA22j54zkKDkzUS1aaN5fd5Ml \r\ngo_to_kitchen_object_detection.mp4: https://drive.google.com/uc?id=1Zx32f07FiZ9Tjhz_g_rNe8vBpN8fL_64 \r\ngo_to_kitchen_panorama.mp4: https://drive.google.com/uc?id=1LjMNvauNfCRBwyqZm24JuLcURGekKbEJ \r\ngo_to_kitchen_rviz.mp4: https://drive.google.com/uc?id=1oTmw2-jXzVX2rTD65shhzTHyHel4xJrD \r\ngo_to_kitchen_audio.wav: https://drive.google.com/uc?id=1kQy4rTpt4WKeVroOVwRoFJtxkaWqSAH5 \r\ngo_to_kitchen_rosbag.bag: https://drive.google.com/uc?id=1rNuEE3gveNsUfTsyHg1Ud5QVL6hc5clC \r\n\r\nFollowing smach is reported.\r\n - At 2022-08-23T13:30:23, Active states is REPORT-START-GO-TO-KITCHEN.\r\n - At 2022-08-23T13:30:26, Active states is GET-LIGHT-ON.\r\n - At 2022-08-23T13:30:28, Active states is REPORT-LIGHT-ON.\r\n - At 2022-08-23T13:30:30, Active states is MOVE-TO-DOCK-FRONT.\r\n - At 2022-08-23T13:30:41, Active states is INSPECT-DOCK-FRONT.\r\n - At 2022-08-23T13:30:54, Active states is MOVE-TO-TV-FRONT.\r\n - At 2022-08-23T13:31:00, Active states is INSPECT-TV-FRONT.\r\n - At 2022-08-23T13:31:15, Active states is MOVE-TO-TV-DESK.\r\n - At 2022-08-23T13:33:01, Active states is INSPECT-TV-DESK.\r\n - At 2022-08-23T13:33:16, Active states is MOVE-TO-DESK-BACK.\r\n\r\n\r\n']

def get_gdrive_url(mail_body_list):
    for i in range(len(mail_body_list)):
        print(i)
        print(mail_body_list[0])
        gdrive_file_pair = [x for x in mail_body_list[i].splitlines() if ': https://drive.google.com' in x]
        print(gdrive_file_pair)
        file_dict = {}
        for j in range(len(gdrive_file_pair)):
            gdrive_file_url = gdrive_file_pair[j].split(': ')
            tmp_dict = dict((gdrive_file_url, ))
            file_dict.update(tmp_dict)
            print(gdrive_file_url)
        print(file_dict)

        for k in file_dict:
            print(k)

        return file_dict

get_gdrive_url(mail_body_list)
