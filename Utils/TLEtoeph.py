# coding: utf-8
import ephem
import math
import datetime
import os


class TLEtoeph(object):
    """
    This class defines the contents of the antenna boot data file.
    Get Eph file from tle file solution.
    """

    def __init__(self, latitude, longtitude, elevation):
        """
        init the location.
        """
        try:
            self.location = ephem.Observer()
            self.location.lon = str(longtitude)
            self.location.lat = str(latitude)
            self.location.elevation = elevation
        except Exception as e:
            print(e)

    def tletoeph(self, pathin, pathoff, time):
        # TLE文件
        with open(pathin, "r")as file:
            n = 0
            data = {}
            for line in file.readlines():
                data[n] = line.strip()
                n += 1
        # 解算
        sat = ephem.readtle(data[0], data[1], data[2])
        # location.date = ephem.now()
        start_time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        start_date = f'{start_time.strftime("%Y%m%d%H%M%S")}'

        if not os.path.exists(pathoff):
            os.makedirs(pathoff)

        file_name = f"{data[0]}_{start_date}.eph"
        full_path = pathoff + '/' + file_name

        with open(full_path, "w") as f:
            tx_stop = 1
            tx_count = 0
            while tx_stop:
                processtime = start_time + datetime.timedelta(seconds=+tx_count)
                self.location.date = (processtime + datetime.timedelta(hours=-8)).strftime("%Y/%m/%d %H:%M:%S")
                utc8date = processtime.strftime("%Y/%m/%d %H:%M:%S")
                tx_count += 1
                sat.compute(self.location)
                if math.degrees(sat.alt) > 1E-7:
                    pitch = ('%.3f' % math.degrees(sat.alt))  # 卫星的俯仰角
                    azimuth = ('%.3f' % math.degrees(sat.az))  # 卫星的方位角
                    f.write(f"{utc8date} {pitch} {azimuth}\n")
                else:
                    tx_stop = 0
            if tx_count > 1:
                print('Solution complete')
            elif tx_count == 1:
                print('Solution failed, Create file is empty')
            else:
                print('Solution failed')


if __name__ == "__main__":
    """
    test class
    """
    t = TLEtoeph(45.7418, 126.6303, 149)
    t.tletoeph('./CSS(TIANHE-1).txt', '/Users/yangjiahao/PycharmProjects/tle-eph', "2021-10-05 04:59:05")