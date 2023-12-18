def main():
    resposts_list = []
    print("responda com s ou n")
    is_t = input("A água está transparente?")
    resposts_list.append(is_t)
    is_c = input("A àgua não tem cheiro?")
    resposts_list.append(is_c)

    goal = len(resposts_list)
    count = 0
    for i in resposts_list:
        if(i == "s"):
            count += 1

    if(count >= goal/2):
        print("É potável")
        return
    
    print("nNão potável")

if __name__ == "__main__":
    main()

