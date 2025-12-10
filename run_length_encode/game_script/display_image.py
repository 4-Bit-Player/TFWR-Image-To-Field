from img_data import get_img



def main():
    # Just run this file to execute it. :)
    # You can execute the image_simulation file to run it at a faster speed.

    img_list = get_img()

    # enter a negative number if it should loop indefinitely
    repeats = -1

    display_image(img_list, repeats)



def should_soil():
    if get_ground_type() != Grounds.Soil:
        till()
        return
    if get_entity_type() != None:
        harvest()

def should_soil_grass():
    if get_ground_type() != Grounds.Soil:
        till()
    if get_entity_type() != Entities.Grass:
        harvest()
        plant(Entities.Grass)


def should_grass_grass():
    if get_ground_type() != Grounds.Grassland:
        till()
        return
    if get_entity_type() != Entities.Grass:
        harvest()

def should_pumpkin():
    if get_ground_type() != Grounds.Soil:
        till()
    if get_entity_type() != Entities.Pumpkin:
        harvest()
        plant(Entities.Pumpkin)

def should_carrots():
    if get_ground_type() != Grounds.Soil:
        till()
    if get_entity_type() != Entities.Carrot:
        harvest()
        plant(Entities.Carrot)

def should_soil_bush():
    if get_ground_type() != Grounds.Soil:
        till()
    if get_entity_type() != Entities.Bush:
        harvest()
        plant(Entities.Bush)

def should_grass_bush():
    if get_ground_type() != Grounds.Grassland:
        till()
    if get_entity_type() != Entities.Bush and get_entity_type() != Entities.Grass:
        harvest()
    plant(Entities.Bush)

def should_soil_tree():
    if get_ground_type() != Grounds.Soil:
        till()
    if get_entity_type() != Entities.Tree:
        harvest()
        plant(Entities.Tree)

def should_grass_tree():
    if get_ground_type() != Grounds.Grassland:
        till()
    if get_entity_type() != Entities.Tree and get_entity_type() != Entities.Grass:
        harvest()
    plant(Entities.Tree)

def should_sunflower():
    if get_ground_type() != Grounds.Soil:
        till()
    if get_entity_type() != Entities.Sunflower:
        harvest()
        plant(Entities.Sunflower)


FUNC_LOOKUP = [should_carrots, should_soil_tree, should_grass_tree, should_soil, should_grass_bush, should_sunflower, should_soil_grass, should_grass_grass, should_pumpkin]
FUNC_DICT = {
    "0": should_carrots,
    "1": should_soil_tree,
    "2": should_grass_tree,
    "3": should_soil,
    "4": should_grass_bush,
    "5": should_sunflower,
    "6": should_soil_grass,
    "7": should_grass_grass,
    "8": should_pumpkin,
}
DECODER = {"a":1,"b":2,"c":3,"d":4,"e":5,"f":6,"g":7,"h":8,"i":9,"j":10,"k":11,"l":12,"m":13,"n":14,"o":15,"p":16,
           "q":17,"r":18,"s":19,"t":20,"u":21,"v":22,"w":23,"x":24,"y":25,"z":26,"A":27,"B":28,"C":29,"D":30,"E":31,
           "F":32,"G":33,"H":34,"I":35,"J":36,"K":37,"L":38,"M":39,"N":40,"O":41,"P":42,"Q":43,"R":44,"S":45,"T":46,
           "U":47,"V":48,"W":49,"X":50,"Y":51,"Z":52,"0":53,"1":54,"2":55,"3":56,"4":57,"5":58,"6":59,"7":60,"8":61,
           "9":62,"ö":63,"ä":64,"ü":65,"#":66,"$":67,"%":68,"&":69,"'":70,"(":71,")":72,"*":73,"+":74,",":75,"-":76,
           ".":77,"/":78,":":79,";":80,"<":81,"=":82,">":83,"?":84,"@":85,"[":86,"Ö":87,"]":88,"^":89,"_":90,"`":91,
           "{":92,"|":93,"}":94,"~":95,"!":96,}

##### Boch Sleep functions copied from my base library.
def sleep_tick(ticks):
    # minimum 3 ticks
    for _ in range(ticks-3):
        pass
    return

# The shenanigans with this are made to improve the simulation performance of multiple drones.
# It can be around 3-6x as fast as the sleep_tick function.
def imprecise_sleep(ticks):
    # minimum 6 ticks
    if ticks < 35:
        return sleep_tick(ticks-3)

    if ticks > 211:
        set_execution_speed(-1)
        if ticks < 240:
            return sleep_tick(ticks-207)
        if ticks > 412:
            set_execution_speed(-1)
            return sleep_tick(ticks-409)
        ticks -= 205

    c = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15, 16, 17, 18, 19]
    required = (ticks - 33) // 20
    rest = ticks - required*20 - 33
    for _ in range(required):
        a = c[:]
    for _ in range(rest):
        pass

#####


def sub_func(lines, direction, repeats=1):
    start_tick = get_tick_count()
    if direction == West:
        move(West)
        iterator = range(len(lines)-2, -1, -2)
    else:
        iterator = range(0, len(lines), 2)
    while num_drones() != 32:
        pass
    if get_tick_count()-start_tick > 250:
        sleep_tick(400)
    else:
        sleep_tick(200 - (get_tick_count()-start_tick))

    if repeats < 0:
        while True:
            _dec_plant_iterator(lines, iterator, direction)
            continue
    else:
        for _ in range(repeats):
            _dec_plant_iterator(lines, iterator, direction)
            continue



def _plant_iterator(line, iterator, move_dir):
    for i in iterator:
        start_ticks = get_tick_count()
        FUNC_DICT[line[i]]()
        imprecise_sleep(420 - (get_tick_count()-start_ticks))
        move(move_dir)

def _dec_plant_iterator(line, iterator, move_dir):
    # iterator right (east): range(0, len(line), 2); iterator left (West): range(len(line)-1, -1, -2)
    start_ticks = get_tick_count()
    for i in iterator:
        func = FUNC_DICT[line[i+1]]
        for _ in range(DECODER[line[i]]):
            func()
            imprecise_sleep(430 - (get_tick_count() - start_ticks))
            move(move_dir)
            start_ticks = get_tick_count()


def display_image(img_list, repeats=1):
    clear()
    for i in range(len(img_list)-1):
        move(South)
        current_line = img_list[i]
        if i % 2:
            direction = West
        else:
            direction = East
        def drone_func():
            sub_func(current_line, direction, repeats)
        spawn_drone(drone_func)

    move(South)
    sub_func(img_list[-1], West, repeats)
    while num_drones() != 1:
        continue


if __name__ == '__main__':
    main()