import sys
from recStripProc import *


class Monitor(object):

    def __init__(self, recording_inputs_path):
        super(Monitor, self).__init__()
        self.audio_in = []
        self.phisio_in = []
        self.loc = []
        self.audio_path = recording_inputs_path
        self.rec_strips_list = []
        self.strips_scores_list = []
        self.strips_alerts_list = []
        self.scores_gradient = 0
        self.alerts_gradient = 0
        self.strip_size = 20 #sec

   def input2strips(self):
        # this method splits the recording input file into strips
        samps_per_sec, audio = read(self.audio_path)
        audio_len = len(audio) / samps_per_sec
        if(audio_len < 20):
            self.rec_strips_list.append(audio)
            return
        strip_len = self.strip_size * samps_per_sec # 20 * samps_per_sec
        i = 0
        while(i + strip_len < len(audio)):
            self.rec_strips_list.append(audio[i:i+strip_len])
            i += strip_len + 1
        self.rec_strips_list.append(audio[i:len(audio)])
        return


def main():
    # get input file
    input_data = "/Users/shimriteliezer/Documents/hackathon/ogg2wav_184214.wav"
    # init Vio Monitor
    # loop on strips (TBD)

    # init record strip
    new_record = RecordStrip(input_data)
    new_record.proc_sensors()
    new_record.get_tot_score()

    print(new_record.tot_score)

    return 0


if __name__ == '__main__':
    try:
        status = main()
        sys.exit(status)
    except KeyboardInterrupt:
        print("")
        print("monitor terminated.")
        sys.exit(1)
