'''
    @param: ISODuration: Duration of the track in ISO Format. 
    @return videoDuration: Duration of the track in milliseconds.
    @description: This function converts the duration of the track from ISO Format to milliseconds by analysing every permuation of the format.
'''
def getTrackDurationYT(ISODuration):
    # print(ISODuration)
    
    if 'H' in ISODuration and 'M' in ISODuration and 'S' in ISODuration:
        videoDuration = int(ISODuration[ISODuration.find('T')+1:ISODuration.find('H')])*3600000 + int(ISODuration[ISODuration.find('H')+1:ISODuration.find('M')])*60000 + int(ISODuration[ISODuration.find('M')+1:ISODuration.find('S')])*1000
    elif 'H' in ISODuration and 'M' in ISODuration:
        videoDuration = int(ISODuration[ISODuration.find('T')+1:ISODuration.find('H')])*3600000 + int(ISODuration[ISODuration.find('H')+1:ISODuration.find('M')])*60000
    elif 'H' in ISODuration and 'S' in ISODuration:
        videoDuration = int(ISODuration[ISODuration.find('T')+1:ISODuration.find('H')])*3600000 + int(ISODuration[ISODuration.find('H')+1:ISODuration.find('S')])*1000
    elif 'M' in ISODuration and 'S' in ISODuration:
        videoDuration = int(ISODuration[ISODuration.find('T')+1:ISODuration.find('M')])*60000 + int(ISODuration[ISODuration.find('M')+1:ISODuration.find('S')])*1000
    elif 'H' in ISODuration:
        videoDuration = int(ISODuration[ISODuration.find('T')+1:ISODuration.find('H')])*3600000
    elif 'M' in ISODuration:
        videoDuration = int(ISODuration[ISODuration.find('T')+1:ISODuration.find('M')])*60000
    elif 'S' in ISODuration:
        videoDuration = int(ISODuration[ISODuration.find('T')+1:ISODuration.find('S')])*1000
    else:
        videoDuration = 0
    
    return videoDuration

