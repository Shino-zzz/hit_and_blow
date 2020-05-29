import itertools

# 要素の種類をキー、その要素の個数を値として格納した辞書を引数として渡すと、組み合わせパターンを返してくれる関数
def combination_pattern(**kwargs):
    l = []
    combination = []

    for k, v in kwargs.items():
        l.append([k]*v)
    # l = [['Hit'], [], ['other', 'other']]のようになる

    for i in range(len(l)):
        combination.extend(l[i])
    # combination = ['Hit', 'other', 'other']のようになる

    return combination

# 要素の種類をキー、その要素の個数を値として格納した辞書を引数として渡すと、順列パターンを返してくれる関数
def permutation_pattern(**kwargs):
    l = combination_pattern(**kwargs)
    permutation = list(set(itertools.permutations(l)))
    #permutation = [('other', 'other', 'Hit'), ('other', 'Hit', 'other'), ('Hit', 'other', 'other')]のようになる
    r = list(map(list, permutation))
    return r

# 各桁の候補から3桁の組み合わせパターンを作る関数
def group_combination(l1, l2, l3):
    product = list(itertools.product(l1, l2, l3))
    list_before = list(map(list, product))
    list_after = []
    for i in range(len(list_before)):
        a = sorted(list(set(list_before[i])), key=list_before[i].index)
        if len(a) == 3:
            list_after.append(a)
    return list_after

# リスト内に3桁の整数の情報が入ったリスト→3桁の整数が入った集合に変換
def convert_to_3digit(l):
    s = set()
    for i in range(len(l)):
        s.add(l[i][0] + l[i][1] * 10 + l[i][2] * 100)
    return s


# 与えられた['Blow', 'other', 'Blow']などの順列パターンから[order_Hit, order_Blow, order_other]を生み出す関数
def check_order(*args):
    order_Hit = []
    order_Blow = []
    order_other = []
    order_info = [order_Hit, order_Blow, order_other]

    for i in range(len(args)):
        if args[i] == 'Hit':
            order_Hit.append(i)

        elif args[i] == 'Blow':
            order_Blow.append(i)

        else:
            order_other.append(i)

    return order_info

def check_candidate_noBlow(*args):
    """
    Blowがない場合に、try_list, ['Hit', 'other', 'other']パターン, order_Hit, order_other
    の情報から候補となる3桁の数字が入ったリストを返す関数

    args[0] にtry_listを代入する予定
    args[1] に['Hit', 'other', 'other']を代入する予定
    args[2] にorder_Hitを代入する予定
    args[3] にorder_otherを代入する予定
    """
    # print(args[0])
    # print(args[1])
    # print(args[2])
    # print(args[3])

    candidate_1 = list(range(10))
    candidate_2 = list(range(10))
    candidate_3 = list(range(10))
    candidate_integrated = [candidate_1, candidate_2, candidate_3]

    # Hitが存在する場合
    if 'Hit' in args[1]:
        for i in range(len(args[2])):
            order_of_Hit = args[2][i]
            # print('try_list中の' + str(order_of_Hit) + '番目に対応する数字がHit')
            num_of_Hit = args[0][order_of_Hit]
            # print('try_list中の数字' + str(num_of_Hit) + 'がHit')

            if order_of_Hit == 0:
                candidate_1.clear()
                candidate_1.append(num_of_Hit)

            if order_of_Hit == 1:
                candidate_2.clear()
                candidate_2.append(num_of_Hit)

            if order_of_Hit == 2:
                candidate_3.clear()
                candidate_3.append(num_of_Hit)

    # print('candidate_1:\n', candidate_1)
    # print('candidate_2:\n', candidate_2)
    # print('candidate_3:\n', candidate_3)

    # otherが存在する場合
    if 'other' in args[1]:
        for j in range(len(args[3])):
            order_of_other = args[3][j]
            # print('try_list中の' + str(order_of_other) + '番目に対応する数字がother')
            num_of_other = args[0][order_of_other]
            # print('try_list中の数字' + str(num_of_other) + 'がother')

            # 3つのリストcandidate_1, candidate_2, candidate_3からnum_of_otherを削除
            for k in range(len(candidate_integrated)):
                if num_of_other in candidate_integrated[k]:
                    candidate_integrated[k].remove(num_of_other)
            candidate_1 = candidate_integrated[0]
            candidate_2 = candidate_integrated[1]
            candidate_3 = candidate_integrated[2]


    # print('candidate_1:\n', candidate_1)
    # print('candidate_2:\n', candidate_2)
    # print('candidate_3:\n', candidate_3)

    candidate = group_combination(candidate_1, candidate_2, candidate_3)
    set_of_candidates = list(convert_to_3digit(candidate))

    return set_of_candidates

def Hit_checker(l1, l2, l3):
    """
    before_listの中のそれぞれのリストについて、Hitの条件を全て満たすものをafter_listとして返す関数
    l1 にbefore_list
    l2 にorder_Hit
    l3 にtry_list
    return  はafter_list
    """
    after_list = []

    for i in range(len(l1)):
        l = l1[i]  # lは[0, 7, 9]とか

        L = []
        for j in range(len(l2)):
            if l[l2[j]] == l3[l2[j]]:
                L.append(1)
            else:
                L.append(0)

        if L.count(1) == len(l2):
            after_list.append(l)

    return after_list


def Blow_checker(l1, l2, l3):
    """
    before_listの中のそれぞれのリストについて、Blowの条件を全て満たすものをafter_listとして返す関数
    l1 にbefore_list (Hitの条件で絞った後のリストを入れる)
    l2 にorder_Blow
    l3 にtry_list
    return  はafter_list
    """
    after_list = []

    for i in range(len(l1)):
        l = l1[i]  # lは[0, 7, 9]とか

        L = []
        for j in range(len(l2)):
            if l[l2[j]] != l3[l2[j]]:
                L.append(1)
            else:
                L.append(0)

        if L.count(1) == len(l2):
            after_list.append(l)

    return after_list


# ここから実行

# 候補群Aの初期状態の設定
all_list = list(group_combination(list(range(10)), list(range(10)), list(range(10))))
A = convert_to_3digit(all_list)

while len(A) > 1:

    """
    入力パート
    """

    # 入力した3桁の整数を各桁ごとに分けてtry_listというリストにする
    try_num = int(input('Please enter a 3-digit number:'))
    try_3rd = try_num // 100
    try_2nd = (try_num % 100) // 10
    try_1st = (try_num % 100) % 10
    try_list = [try_1st, try_2nd, try_3rd]

    # 入力したHitの個数、Blowの個数を元にhitとblowとotherの組み合わせをつくる
    hit_num = int(input('How many Hits did you get?:'))
    blow_num = int(input('How many Blows did you get?:'))
    other_num = 3 - (hit_num + blow_num)

    # HitとBlowの種類と個数の対応を辞書にしておく
    Hit_Blow_Num = {'Hit': hit_num, 'Blow': blow_num, 'other': other_num}

    # hit_blow_typeを生成する
    hit_blow_type = permutation_pattern(**Hit_Blow_Num)
    # print('hit_blow_typeの中身は:\n', hit_blow_type)

    """
    ここから、hit_blow_type[i]の場合に応じてリストb内に候補となるリストを追加していく
    """

    b = []

    for i in range(len(hit_blow_type)):
        if 'Blow' in hit_blow_type[i]:
            """
            あとはここを書けば1回分のループは完了！
            """
            order_Hit = check_order(*hit_blow_type[i])[0]
            order_Blow = check_order(*hit_blow_type[i])[1]
            order_other = check_order(*hit_blow_type[i])[2]

            # 全順列(6通り)列挙
            before_list = list(map(list, list(itertools.permutations(try_list))))
            #print(before_list)

            # HitとBlowの条件からフィルタリング
            result1 = Hit_checker(before_list, order_Hit, try_list)
            result2 = Blow_checker(result1, order_Blow, try_list)

            # 'Hit'と'other'のパターンを作成する
            for i in range(len(result2)):
                l = result2[i]  # [7, 0, 9]とか

                # 初期状態を作る
                hit_other_type = []
                for j in range(len(result2)):
                    hit_other_type.append(['Hit', 'Hit', 'Hit'])

                for k in range(len(order_other)):
                    order_of_other = order_other[k]
                    num_of_other = try_list[order_of_other]

                    # 上書きする
                    hit_other_type[i][l.index(num_of_other)] = 'other'

                new_order_Hit = check_order(*hit_other_type[i])[0]
                new_order_other = check_order(*hit_other_type[i])[2]

                b.append(check_candidate_noBlow(result2[i], hit_other_type[i], new_order_Hit, new_order_other))

        # Blowがない場合
        else:
            # リストorder_Hit, order_Blow, order_otherを求める
            order_Hit = check_order(*hit_blow_type[i])[0]
            order_Blow = check_order(*hit_blow_type[i])[1]
            order_other = check_order(*hit_blow_type[i])[2]

            # 候補の数字が入ったリストを、リストbに追加する
            b.append(check_candidate_noBlow(try_list, hit_blow_type[i], order_Hit, order_other))

    """
    最後に和集合をとって、この試行の結果から導かれる候補の集合Bを作り、表示
    """

    # リストb内の各リストを集合にして、それらの集合の和をとり、候補群Bに入れる
    B = set()
    for i in range(len(b)):
        B = B | set(b[i])
        # print(str(i) + '回目のB:' + str(B))

    A = A & B

    # 表示
    print('The candidate numbers are the following'+ str(len(A)))
    print(A)

else:
    print('You did it!')


