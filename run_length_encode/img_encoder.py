import string


_ENCODE_CHARS = string.ascii_lowercase + string.ascii_uppercase + string.digits + r"öäü#$%&'()*+,-./:;<=>?@[Ö]^_`{|}~!"
_decoder_str = '{"a":1,"b":2,"c":3,"d":4,"e":5,"f":6,"g":7,"h":8,"i":9,"j":10,"k":11,"l":12,"m":13,"n":14,"o":15,"p":16,"q":17,"r":18,"s":19,"t":20,"u":21,"v":22,"w":23,"x":24,"y":25,"z":26,"A":27,"B":28,"C":29,"D":30,"E":31,"F":32,"G":33,"H":34,"I":35,"J":36,"K":37,"L":38,"M":39,"N":40,"O":41,"P":42,"Q":43,"R":44,"S":45,"T":46,"U":47,"V":48,"W":49,"X":50,"Y":51,"Z":52,"0":53,"1":54,"2":55,"3":56,"4":57,"5":58,"6":59,"7":60,"8":61,"9":62,"ö":63,"ä":64,"ü":65,"#":66,"$":67,"%":68,"&":69,"\'":70,"(":71,")":72,"*":73,"+":74,",":75,"-":76,".":77,"/":78,":":79,";":80,"<":81,"=":82,">":83,"?":84,"@":85,"[":86,"Ö":87,"]":88,"^":89,"_":90,"`":91,"{":92,"|":93,"}":94,"~":95,"!":96,}'


def get_game_decoder_string() -> str:
    return "def get_decoder():\n    return " + _decoder_str + "\n"

_encoder_char_index = 0

def _get_next_enc_char() -> str:
    global _encoder_char_index
    if _encoder_char_index >= len(_ENCODE_CHARS):
        raise ValueError("Logic Error in run length encoder!\nRequested more encoding chars than available!")
    char = _ENCODE_CHARS[_encoder_char_index]
    _encoder_char_index += 1
    return char




def run_length_encode(line_arr:list[str]) -> list[str]:
    counter = {}
    available_encode_chars = len(_ENCODE_CHARS)
    for line in line_arr:
        count = 0
        char = line[1]
        for i in range(len(line)):
            if line[i] == '"':
                continue
            if line[i] == char:
                count += 1
                continue
            if count not in counter:
                counter[count] = 1
                if len(counter) >= available_encode_chars:
                    break
            char = line[i]
            count = 1
        if count != 0:
            if count not in counter:
                counter[count] = 1
        if len(counter) >= available_encode_chars:
            break

    if len(counter) >= available_encode_chars:
        return _default_encoder(line_arr)
    return _custom_encoder(line_arr)



def _default_encoder(line_arr:list[str]) -> list[str]:
    encoder = {1:"a",2:"b",3:"c",4:"d",5:"e",6:"f",7:"g",8:"h",9:"i",10:"j",11:"k",12:"l",13:"m",14:"n",15:"o",16:"p",17:"q",18:"r",19:"s",20:"t",21:"u",22:"v",23:"w",24:"x",25:"y",26:"z",27:"A",28:"B",29:"C",30:"D",31:"E",32:"F",33:"G",34:"H",35:"I",36:"J",37:"K",38:"L",39:"M",40:"N",41:"O",42:"P",43:"Q",44:"R",45:"S",46:"T",47:"U",48:"V",49:"W",50:"X",51:"Y",52:"Z",53:"0",54:"1",55:"2",56:"3",57:"4",58:"5",59:"6",60:"7",61:"8",62:"9",63:"ö",64:"ä",65:"ü",66:"#",67:"$",68:"%",69:"&",70:"'",71:"(",72:")",73:"*",74:"+",75:",",76:"-",77:".",78:"/",79:":",80:";",81:"<",82:"=",83:">",84:"?",85:"@",86:"[",87:"Ö",88:"]",89:"^",90:"_",91:"`",92:"{",93:"|",94:"}",95:"~",96:"!",}
    out:list[str]=[]

    for line in line_arr:
        new_line:list[str] = []
        char = line[0]
        count = 0
        for i in range(len(line)):
            if line[i] == '"':
                continue
            if line[i] == char:
                count += 1
                if count == len(encoder):
                    new_line.append(f"{encoder[count]}{char}")
                    count = 0
                continue
            if count != 0:
                new_line.append(f"{encoder[count]}{char}")
            char = line[i]
            count = 1
        if count != 0:
            new_line.append(f"{encoder[count]}{char}")
        out.append('"'+ "".join(new_line) + '"')
    return out



def _custom_encoder(line_arr:list[str]) -> list[str]:
    global _decoder_str

    out:list[str]=[]
    decoder:dict[str, int] = {}
    encoder:dict[int, str] = {}
    for line in line_arr:
        new_line:list[str] = []
        char = line[0]
        count = 0
        for i in range(len(line)):
            if line[i] == '"':
                continue
            if line[i] == char:
                count += 1
                continue
            if count != 0:
                if count in encoder:
                    enc_char = encoder[count]
                else:
                    enc_char = _get_next_enc_char()
                    encoder[count] = enc_char
                    decoder[enc_char] = count
                new_line.append(f"{enc_char}{char}")

            char = line[i]
            count = 1
            continue # technically unnecessary, but it makes it more obvious that this is the end of the inner for loop

        if count != 0:
            if count in encoder:
                enc_char = encoder[count]
            else:
                enc_char = _get_next_enc_char()
                encoder[count] = enc_char
                decoder[enc_char] = count
            new_line.append(f"{enc_char}{char}")

        out.append('"'+ "".join(new_line) + '"')

    # creating the custom decoder for the game.
    new_decoder = ["{"]
    for key, val in decoder.items():
        new_decoder.append(f'"{key}":{val},')
    new_decoder.append("}")

    _decoder_str = "".join(new_decoder)


    return out