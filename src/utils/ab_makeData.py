import peppi_py as pp

def pre_frame_dict(frame, port):
    out_dict = {}
    frameData = frame['ports'][port]['leader']['pre']
    val = [
    {'x_pos' : frameData['position']['x'].as_py()},
    {'y_pos' : frameData['position']['y'].as_py()},
    {'x_joy' : frameData['joystick']['x'].as_py()},
    {'y_joy' : frameData['joystick']['y'].as_py()},
    {'buttons': frameData['buttons'].as_py()},
    {'percent': frameData['percent'].as_py()}
    ]

    for x in val: 
        out_dict.update(x)

    return out_dict



def post_frame_dict(frame, port):
    out_dict = {}
    frameData = frame['ports'][port]['leader']['post']
    val = [
    {'x_pos' : frameData['position']['x'].as_py()},
    {'y_pos' : frameData['position']['y'].as_py()},
    {'percent': frameData['percent'].as_py()}
    ]

    for x in val: 
        out_dict.update(x)
        
    return out_dict
    
def makeInputDict(frame, port):
    ## fix later
    out_dict = {}
    preData =  frame['ports'][port]['leader']['pre']
    postData = frame['ports'][port]['leader']['post']

    val = [
    {'x_pos' : postData['position']['x'].as_py()},
    {'y_pos' : postData['position']['y'].as_py()}
    ]





def make_pre_large(game : pp.Game):

    ports = []
    characters = []
    for player in game.start['players']:
        port = player['port']
        ports.append(port)
        characters.append(player['character'])
    
    out_list = []
    
    for playerIndex, port in enumerate(ports):
        for framenumber, frame in enumerate(game.frames):
            pre_out = pre_frame_dict(frame, port)
            pre_out.update({"Player" : str(playerIndex)})
            pre_out.update({"frameNumber" : str(framenumber)})
            pre_out.update({'stage' : str(game.start['stage'])})
            pre_out.update({'character' : str(characters[playerIndex])})
            out_list.append(pre_out)

    return out_list


def make_post_large(game : pp.Game):

    ports = []
    for player in game.start['players']:
        port = player['port']
        ports.append(port)
    
    out_list = []
    for playerIndex, port in enumerate(ports):
        for framenumber, frame in enumerate(game.frames):
            pre_out = post_frame_dict(frame, port)
            pre_out.update({"Player" : str(playerIndex)})
            pre_out.update({"frameNumber" : str(framenumber)})
            out_list.append(pre_out)

    print(len(out_list))
    return out_list
        