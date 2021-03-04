def get_information_agent(location):
    base_infect=0.03
    # locations: "Work","School","Shop","Bar","Park","University"
    p1 = []
    p2 = ["Work","Home","School"]
    p3 = ["University"]
    p4 = ["Shop"]
    p5 = ["Bar","Park"]



    if location in p1:
        return base_infect

    elif lcocation in p2:
        return base_infect/2
    
    elif lcocation in p3:
        return base_infect/4

    elif lcocation in p4:
        return base_infect/8

    elif lcocation in p5:
        return base_infect/16
    
    else:
        return base_infect