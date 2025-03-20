# from project import class
# from project.file import class
import csv
import os
#import time

class UzMorphAnalyser:
    __affixes = []  # list of affixes table from affixes.csv file
    __small_stems = []  # list of small stems from small_stems.csv file
    __non_affixed_stems = []  # list of non affixed stems from non_affixed_stems.csv file
    __number_stems = []  # list of number stems from number_stems.csv file
    __exception_stems = []  # list of exception stems from exception_stems.csv file
    __lemma_map = []  # list of lemma convertion mapping from lemma_map.csv file
    # __ambiguity_stems = []  # list of ambiguity stems from ambiguity_stems.csv file | oxiri affix bn tugaydigan asos suzlar

    __vovel = ['a', 'u', 'e', 'i', 'o',"o'"]
    __consonant_hard = ['b', 'd', 'g', 'j', 'l', 'm', 'n', 'r', 'v', 'y', 'z', "g'", 'ng']  # jarangli undosh
    __consonant_soft = ['f', 'h', 'k', 'p', 'q', 's', 't', 'x', 'sh', 'ch']  # jarangsiz undosh
    __consonant = ['b', 'd', 'g', 'j', 'l', 'm', 'n', 'r', 'v', 'y', 'z', 'f', 'k', 'p', 'q', 's', 't', 'x', 's', 'c', 'h' ]  # all undosh

    # affixes.csv da barcha allomorphlarni qulda generate qilib yozib quyamiz, dastur yordamida qilmaymiz, chalkash joylari kup
    # bu generate funksiya faqat qavs ichida bitta harf (katta/kichik) turganda va bitta katta harf mavjud bulganda tugri keladi.
    def __GeneratedAllomorph(self, affix):  # return a list that contain all allomorphs of the current affix
        GenAff = []
        # if allomorph has omitted letter # qavsli faqat affix boshida keladi
        parentesis = False  # is exist parentesis
        affix_v1, affix_v2 = "", ""  # v1-qavs ichidagi bn, v2-qavs ichidagisiz qushimcha
        uc_v1, uc_v2 = -1, -1  # postion of uppercase in affix

        if affix[0] == "(":
            affix_v1 = affix.replace("(", "").replace(")", "")  # affix[1]+affix[3:] #qavs ichidagi bilan olish
            affix_v2 = affix[affix.find(")") + 1:]  # qavs ichidagisiz olish
            parentesis = True
        else:
            affix_v1 = affix

        # if allomorph has uppper letter (several letters)
        for i in range(len(affix_v1)):
            if affix_v1[i].isupper():
                uc_v1 = i
                break
        for i in range(len(affix_v2)):
            if affix_v2[i].isupper():
                uc_v2 = i
                break
        '''if affix == '(S)i':
            print('-----------')
            print(affix_v1)
            print(affix_v2)
            print(uc_v1)
            print(uc_v2)
        '''
        if uc_v1 > -1:  # katta harfi bulgan varianti
            if affix_v1[uc_v1] == "G":  # G:g,k,q
                GenAff.append(affix_v1[:uc_v1] + "g" + affix_v1[uc_v1 + 1:])
                GenAff.append(affix_v1[:uc_v1] + "k" + affix_v1[uc_v1 + 1:])
                GenAff.append(affix_v1[:uc_v1] + "q" + affix_v1[uc_v1 + 1:])
            if affix_v1[uc_v1] == "K":  # K:g,k
                GenAff.append(affix_v1[:uc_v1] + "g" + affix_v1[uc_v1 + 1:])
                GenAff.append(affix_v1[:uc_v1] + "k" + affix_v1[uc_v1 + 1:])
            if affix_v1[uc_v1] == "Y":  # Y:a,y
                GenAff.append(affix_v1[:uc_v1] + "a" + affix_v1[uc_v1 + 1:])
                GenAff.append(affix_v1[:uc_v1] + "y" + affix_v1[uc_v1 + 1:])
            if affix_v1[uc_v1] == "T":  # T:t,d
                GenAff.append(affix_v1[:uc_v1] + "t" + affix_v1[uc_v1 + 1:])
                GenAff.append(affix_v1[:uc_v1] + "d" + affix_v1[uc_v1 + 1:])
            if affix_v1[uc_v1] == "Q":  # Q:g,g',k,q
                GenAff.append(affix_v1[:uc_v1] + "g" + affix_v1[uc_v1 + 1:])
                GenAff.append(affix_v1[:uc_v1] + "gʻ" + affix_v1[uc_v1 + 1:])
                GenAff.append(affix_v1[:uc_v1] + "k" + affix_v1[uc_v1 + 1:])
                GenAff.append(affix_v1[:uc_v1] + "q" + affix_v1[uc_v1 + 1:])
            if affix_v1[uc_v1] == "S":  # S:s,y opasi,avzoyi
                GenAff.append(affix_v1[:uc_v1] + "s" + affix_v1[uc_v1 + 1:])
                GenAff.append(affix_v1[:uc_v1] + "y" + affix_v1[uc_v1 + 1:])
            if affix_v1[uc_v1] == "A":  # A:a,i tushir, chiqar
                GenAff.append(affix_v1[:uc_v1] + "a" + affix_v1[uc_v1 + 1:])
                GenAff.append(affix_v1[:uc_v1] + "i" + affix_v1[uc_v1 + 1:])
        else:
            GenAff.append(affix_v1)  # katta harfi bulmagan varianti

        if parentesis:
            if uc_v2 > -1:  # qavsli va katta harfli varianti
                if affix_v2[uc_v2] == "G":  # G:g,k,q
                    GenAff.append(affix_v2[:uc_v2] + "g" + affix_v2[uc_v2 + 1:])
                    GenAff.append(affix_v2[:uc_v2] + "k" + affix_v2[uc_v2 + 1:])
                    GenAff.append(affix_v2[:uc_v2] + "q" + affix_v2[uc_v2 + 1:])
                if affix_v2[uc_v2] == "K":  # K:g,k
                    GenAff.append(affix_v2[:uc_v2] + "g" + affix_v2[uc_v2 + 1:])
                    GenAff.append(affix_v2[:uc_v2] + "k" + affix_v2[uc_v2 + 1:])
                if affix_v2[uc_v2] == "Y":  # Y:a,y
                    GenAff.append(affix_v2[:uc_v2] + "a" + affix_v2[uc_v2 + 1:])
                    GenAff.append(affix_v2[:uc_v2] + "y" + affix_v2[uc_v2 + 1:])
                if affix_v2[uc_v2] == "T":  # T:t,d
                    GenAff.append(affix_v2[:uc_v2] + "t" + affix_v2[uc_v2 + 1:])
                    GenAff.append(affix_v2[:uc_v2] + "d" + affix_v2[uc_v2 + 1:])
                if affix_v2[uc_v2] == "Q":  # Q:g,g',k,q
                    GenAff.append(affix_v2[:uc_v2] + "g" + affix_v2[uc_v2 + 1:])
                    GenAff.append(affix_v2[:uc_v2] + "g‘" + affix_v2[uc_v2 + 1:])
                    GenAff.append(affix_v2[:uc_v2] + "k" + affix_v2[uc_v2 + 1:])
                    GenAff.append(affix_v2[:uc_v2] + "q" + affix_v2[uc_v2 + 1:])
                if affix_v2[uc_v2] == "S":  # S:s,y
                    GenAff.append(affix_v2[:uc_v2] + "s" + affix_v2[uc_v2 + 1:])
                    GenAff.append(affix_v2[:uc_v2] + "y" + affix_v2[uc_v2 + 1:])
                if affix_v2[uc_v2] == "A":  # A:a,i tushir/chiqar
                    GenAff.append(affix_v2[:uc_v2] + "a" + affix_v2[uc_v2 + 1:])
                    GenAff.append(affix_v2[:uc_v2] + "i" + affix_v2[uc_v2 + 1:])
            else:
                GenAff.append(affix_v2)  # qavsli lekin Katta harfsiz varianti
        return GenAff
        # end of Generate Allmorph

    def __init__(self):
        self.__read_data()

    def __read_data(self):
        # url = 'http://u92156l3.beget.tech/affix/export.php', it couldn't be get from url
        dirname = os.path.dirname(__file__) + "/"

        with open(os.path.join(dirname + "affixes.csv"), "r", encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.__affixes = list(reader)

        with open(os.path.join(dirname + "small_stems.csv"), "r", encoding='utf-8') as f:
            reader = csv.reader(f)
            # self.__small_stems = list(reader)
            self.__small_stems = [item for sublist in list(reader) for item in sublist]
        with open(os.path.join(dirname + "non_affixed_stems.csv"), "r", encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.__non_affixed_stems = list(reader)
            # reader = csv.reader(f)
            # self.__non_affixed_stems = [item for sublist in list(reader) for item in sublist]

        with open(os.path.join(dirname + "number_stems.csv"), "r", encoding='utf-8') as f:
            reader = csv.reader(f)
            # self.__small_stems = list(reader)
            self.__number_stems = [item for sublist in list(reader) for item in sublist]
        # with open("ambiguity_stems.csv", "r") as f:
        #    reader = csv.DictReader(f)
        #    self.__ambiguity_stems = list(reader)
        with open(os.path.join(dirname + "exception_stems.csv"), "r", encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.__exception_stems = list(reader)
        with open(os.path.join(dirname + "lemma_map.csv"), "r", encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.__lemma_map = list(reader)

        # generate all allomorphs for each affix and allomorph list to affixes list
        for item in self.__affixes:
            item['allomorphs'] = self.__GeneratedAllomorph(item['affix'])
            # for tt in range(len(item["allomorphs"])):
            #     print(item["allomorphs"][tt])

        # enf of read_data

    def __check_affixation_rules(self, affix: str, word: str, i: int):
        # True = affix qirqilsin, aks holda qirqilmasin
        # 0-rule Suz harflarini joylashuviga kura suz oxirida 2ta unli yoki 2 ta bir xil harfli undosh bilan asos tugamaydi (ikki->ikk), agar bunday hol bulayotgan bulsa, undan bu qushimchani qirqishni otkaz qilamiz. 2 xil undosh bn tugashi mumkin: tort+ib
        buf = word[:i]  # suzni asosidagi oxirgi 2 ta harfni olish
        buf = buf.replace("'", "")
        buf = buf.replace("‘", "")
        if len(buf) >= 3:
            buf1 = buf[-3]  # asosni oxiridan 3-xarfi
            buf = buf[-2:]  # suzni asosidagi oxirgi 2 ta harfni olish

            if len(buf) == 2 and i < 10: # 10 harfdan kichik suzlarni tekshiradi faqat
                if (buf[0] in self.__vovel and buf[1] in self.__vovel) or (buf[0] in self.__consonant and buf[0] == buf[1]) \
                        or (buf[0] in self.__consonant and buf[1] in self.__consonant and buf1 not in self.__vovel):  #(buf[0] in self.__consonant and buf[1] in self.__consonant and buf not in ["ch","sh", "tq", "sm"]) or  # asosdagi oxirgi 2 harfni 2lasi xam unli yoki 2ta bir xil harfli undosh bulsa (ikk)
                    return False

            if (buf[0] in self.__consonant and buf[1] in self.__consonant and buf1 not in self.__vovel):
                # asosdagi unli va undoshla mutanosibligini tekshirish
                vovelcnt = sum(c in self.__vovel for c in word[:i])
                double_char = word[:i].count("ch") + word[:i].count("sh") + word[:i].count("ng") + word[:i].count("sm") + word[:i].count("tq") + word[:i].count("'") +  word[:i].count("‘") # word[:i].count("’") +
                if len(word[:i]) - vovelcnt - double_char > 1:
                    # print(len(word[:i]) - vovelcnt - double_char)
                    if vovelcnt * 2 < len(word[:i]) - vovelcnt - double_char and not (vovelcnt == 1 and len(word[:i]) - vovelcnt - double_char == 3):
                        return False

        # 1.1-rule
        if affix.startswith("(i)m"):  # (i)m egalik qushimchasida, m dan oldin kupincha a harfi keladi, agar bunday bulmasa, bu m qushimchasini qirqamay utirib yuboramiz
            if word[i] == "m" and word[i-1] not in ['a','i']:  # agar oldigi harfi a ga teng bulmasa bunda m ni qirqmasin
                return False  # don't chop, break it
        # 1.2-rule
        if affix.startswith("(s)i"):  # (s)i quchimchasidan oldin a,i harfi keladi. bunday bulmasa, bu m qushimchasini qirqamay utirib yuboramiz
            if word[i] == "s" and word[i-1] not in ['a','i','o','y','u']:  # agar oldigi harfi a ga teng bulmasa bunda m ni qirqmasin
                return False  # don't chop, break it
        # 1.3-rule
        if affix.startswith("(i)b"):  # (i)b  qushimchasi a,i harflaridan keyin qushiladi faqat. aytib,kuylab
            if word[i] == "b" and word[i-1] not in ["i", "a"]:  # bulsa bunda qushimchani qirqmasin
                return False  # don't chop, break it
        # 1.4-rule
        if affix.startswith("(i)sh"):  # (i)sh  qushimchasi a,i harflaridan keyin qushiladi odatda. uxlash,uchish
            if word[i:i+2] == "sh" and word[i-1] not in ["i", "a"]:  # bulsa bunda qushimchani qirqmasin
                return False  # don't chop, break it

        # 2-rule
        if affix.startswith('G'):  # Guncha, Gani,Gan,Gancha,Gani {G=g,k,q}  qushimchasidan oldin k,q harfi kelishi kerak, agar bunday bulmasa bu qushimchani qirqamay utirib yuboramiz
            if (word[i] == "k" and word[i-1] not in ['k']) or (word[i] == "q" and word[i-1] not in ['q']):  # bulsa qushimchani qirqmasin
                return False  # don't chop, break it
        # 3-rule
        if affix.startswith("ir"):  # ir  qushimchasi t,ch,sh harflaridan keyin qushiladi faqat. botir,ichir,shishir
            if word[i-1] not in ["t", "p"] and word[i-2:i] not in ["ch", "sh"]:  # bulsa bunda qushimchani qirqmasin
                return False  # don't chop, break it
        # 4-rule
        if affix.startswith("iz"):  # iz  qushimchasi q,m harflaridan keyin qushiladi faqat. oqiz, tomiz
            if word[i-1] not in ["q", "m"]:  # bulsa bunda qushimchani qirqmasin
                return False  # don't chop, break it

        # 5-rule
        # if affix.__contains__("dagi") and not affix.__contains__("dagina"):  # qirqilayotgan affixda -dagi qushimchasi bulsa, tekshiramiz, shu asos bosh harf bn yozilganmi, chunki dagi faqat atoqli otlarga qushilsa lugaviy qushimcha buladi, boshqa xollarda suz yasovchi buladi
        #     if not word[0].isupper():  # bulsa bunda qushimchani qirqmasin
        #         return False  # don't chop, break it

        # 6-rule
        if word[i:].startswith("i") and word[i-3:i] == "dag":  # -dagi qushimchasidan -i qushimchasini qirqauotgan bulsa buni qirqtirmaymiz, chunki dagini tuliq uizni qirqadi yoki tugri kelmasi qirqmaydi
            return False  # don't chop, break it
        # 7-rule
        if affix.startswith("(i)l"):  # -(i)l:  bo'lgan suzida -(i)lgan qushimchasini qirqib yuboryapti, -(i)l qushimchasidan -l quchimchasi faqat unli bn tugagan asosga qushiladi, bu asoslar kamida 4 harfdan iborat buladi katta ehtimol bn: ajra+lgan
            if word[i] == "l" and i < 4:  # bulsa bunda qushimchani qirqmasin
                return False  # don't chop, break it
        # 8-rule
        if affix.startswith("(i)la"):  # (i)la
            if word[i] == "l" and word[i-1] not in ["a", "i"]:  # bulsa bunda qushimchani qirqmasin
                return False  # don't chop, break it
        # 9-rule
        if affix.startswith("mlar"):  # xurmatlash manosidagi
            if word[i-1] not in ["a"]:  # bulsa bunda qushimchani qirqmasin
                return False  # don't chop, break it

        # 4-rule
        if affix.startswith("iz"):  # iz  qushimchasi q,m harflaridan keyin qushiladi faqat. oqiz, tomiz
            if word[i-1] not in ["q", "m"]:  # bulsa bunda qushimchani qirqmasin
                return False  # don't chop, break it

        # 8-rule  -(s)i kitobi dagi -i ni qirqanda to'g'ri dagi -i ni qirqadi, -i qirqilganda undan oldingi harflarni 2tasi unli+undosh bulsa qirqilsin, aksholda otkaz
        #if affix.startswith("(s)i") and word[i] == "i" and i > 2 and word[i-2:i] not in ['ng','tr','vq','st']: # asosni oxirgi 2 harfi -ng ga teng bulmasa jang+i, metr+i,zavq+i,artist+i da qirqavarsin
        #    if not (word[i-2] in self.__vovel and word[i-1] not in self.__vovel):
        #        return False  # don't chop, break it

        return True  # it is ok, go on chopping

    def __correction_stem_lemma(self, self1, result):
        for item in result:  # result is list
            # I-type: xarf ortishi (avzoy+im->avzo, bun+da->bu)
            # 1-rule [avzoy+im->avzo, (xarf ortishi)] mavqe,azvo,obro',mavzu
            if item['affixed'].startswith("i") and item['stem'][-2:] in ["ey", "oy", "'y"] and len(item['stem']) > 3:
                item['stem'], item['lemma'] = item['stem'][:-1], item['stem'][:-1]
            # 2-rule [bun+da->bu, (xarf ortishi)] unda,unday,bunda,bunday,shunda,shunday, shunga,bunga
            if (item['affixed'].startswith("d") or item['affixed'].startswith("g")) and item['stem'] in ["un", "bun", "shun"]:
                item['stem'], item['lemma'] = item['stem'][:-1], item['stem'][:-1] # remove last letter which is n from stem

            # II-type: Xarf uzgarishi
            # 1-rule [qiyinchilig+i ->qiyinchilik (xarf uzgarishi)]
            if item['affixed'].startswith("i") and item["stem"][-3:] == "lig": # [-3:] = oxirgi 3 harf = "lig" bulsa
                item['lemma'] = item['stem'][:-1] + "k" # item['stem'] ga tegmaymiz uz holicha qoladi "lig" xolida qoladi
            # 2-rule [bilag+i ->bilak (xarf uzgarishi)]
            if item['affixed'].startswith("i") and item["stem"][-2:] == "ag": #  [-2:] = oxirgi 2 harfi = "ag" bulsa
                item['lemma'] = item['stem'][:-1] + "k"
            # 3-rule [o'rtog'+i ->o'rtoq (xarf uzgarishi)]
            if item['affixed'].startswith("i") and item["stem"][-3:] == "og‘": #  [-3:] = oxirgi 3 harfi = "og`" bulsa
                item['lemma'] = item['stem'][:-2] + "q"

        return result
        #end of correction_stem

    #  umumiy holda yani stem, lemma, analyse metodlaridan turib __processing metodidan foydalanamiz

    def __processing(self, word: str, pos: str = None, is_lemmatize: bool = False, multi_item: bool = False):
        affixes = []
        ex_stem_list = []

        affixes_temp = []

        if pos is not None:  # if "pos" argument is given, "pos" argument may be given in lemmatize
            affixes = [i for i in self.__affixes if i['pos'] == pos]
            ex_stem_list = [i for i in self.__exception_stems if i['pos'] == pos]
        else:
            affixes = self.__affixes
            ex_stem_list = self.__exception_stems
            # print(affixes)

        # bu stem_find_exceptions funksiyasi kerak emas, ishlatilmaydi. buni vazifasini boshqa yerda yozdik
        def stem_find_exceptions(self, word: str, position: int):
            for i in range(position, len(word) + 1):  # +1 bu word[:i] i+1 yani oxirgisigacha olishi uchun
                # print("find from excp == " + word[:i])
                ex_stem_find = list(filter(lambda ex_stem: ex_stem['stem'].casefold() == word[:i].casefold(), ex_stem_list))  # pythonic way -> https://stackoverflow.com/questions/8653516/python-list-of-dictionaries-search
                if ex_stem_find:
                    ex_stem_find[0]['stem'] = word[:i]
                    ex_stem_find[0]['lemma'] = word[:i]
                    ex_stem_find[0]['affixed'] = word[i:]
                    #print('found from excp')
                    #print(ex_stem_find)
                    return True, ex_stem_find[0]
                # if word[:i] in ex_stem_list:
                #    return True, {'stem': word[:i], 'pos':}  #return two value, stem from exception
            return False, ""

        def stem_find(self, word: str, pos: str, position: int = 1, res_exist: bool = False): # position = 1 adi
            for i in range(position, len(word)):
                # predict_as_stem = word[:i]
                # predict_as_affix = word[i:]
                result_items1 = []  # list of dictionary [{'stem':'biz', 'affixed':'lar', ...},{...}] bundagi javoblar shunga yigiladi

                # small_stem ni tekshirib olamiz
                affixes_temp = affixes
                if i <= 2:  # i==2 bulsa 0 va 1 belgini oladi, [:2] da 2 ikkini uzi kirmaydi
                    if word[:i].casefold() in self.__small_stems:
                        for item in affixes_temp:
                            if word[i:] in item['allomorphs']:
                                item['stem'], item['lemma'], item['affixed'] = word[:i], word[:i], word[i:]
                                result_items1.append(item)
                    else:
                        continue # 3dan kichik bulgan asosni small_stemdan topmasa qirqmasdan utiramiz, va yana harf qushib asos hosil qiliadi

                if result_items1:
                    return result_items1 # resultni qaytarib beramiz, bu yerdan xam topildi, small_stemdan topildi xarflar buyicha sikl aylanishni tuxtatsak buladi


                affixes_temp = affixes
                for item in affixes_temp:
                    # if word[i:] in self.__GeneratedAllomorph(item["affix"]):
                    if word[i:] in item["allomorphs"]:
                        # print(self.__GeneratedAllomorph(item["affix"]))
                        # print(position)
                        # print(self.__GeneratedAllomorph(item["affix"]))
                        # print(word[:i]+" "+word[i:]+" "+item["affix"])
                        # print(word[i:])
                        # print(item["affix"])
                        # print(self.__exception_stems)
                        # print(item["confidence"])

                        # 6-rule Ga{ga,ka,qa,} bulardan ka, qa g'a uchun undan oldingi xarf shu affixni birinchi harfi bn tugagan bulishi kerak

                        # 1-support rule:
                        '''  bu tashqariga chiqarildi
                        if item['pos'] == self.POS.NUM:
                            if word[:i] in self.__number_stems:
                                item['stem'], item['lemma'], item['affixed'] = word[:i], word[:i], word[i:]  # add stem key_value to item dictionary from affixes
                                result_items1.append(item)
                        '''

                        # check different kind of affixation rules
                        if not self.__check_affixation_rules(item['affix'], word, i):  # xar xil qoidalar, biron qushimchalar buyicha, masalan, (i)m egalik qushimchasida, m dan oldin kupincha a harfi keladi, agar bunday bulmasa, bu m qushimchasini qirqamay utirib yuboramiz
                            continue # qirqmasdan utkazib yuboramiz, keyingi affixlarni tekshirishga

                        # buni xam yuqoriga chiqardik
                        # exception dan suzlarni tekshirib olish
                        '''
                        if len(word[i:]) <= 5:  # 3 bu yerda fine-tuning qilingan, yani 3 harfdan katta qushimchalarda xatolik bulmaydi va bundaylarni tugri qirqsak buladi
                            found_ex, item_ex = stem_find_exceptions(self, word, i + 1)
                            if found_ex:
                                # found_aff = False
                                # for i_affixes in affixes:  # agar exception.csv dan topilsa, undan qolgan qushimchani affixes dan qidirib topib, undagi malumotlarni olamiz
                                #     if item_ex['affixed'] in i_affixes["allomorphs"]:
                                #         i_affixes['stem'], i_affixes['lemma'], i_affixes['affixed'] = item_ex['stem'], item_ex['lemma'], item_ex['affixed']
                                #         result_items.append(i_affixes)
                                #         found_aff = True
                                #         if not multi_item:
                                #             return result_items

                                result_items1.append(item_ex)

                                # break  # agar len(affix)<=3 bulsa va stem exception.csv dan topilmasa, bu affixni qirqmay, navbatdagi affixni yasash uchun bu sikl sindiriladi
                                ###return item_ex  # agar suz exceptionda bor bulsa va unda umuman qushimchasi bulmasa
                        '''

                        # buni tashqariga chiqardik
                        # 2.1-rule qushimchasi topilgandan keyin oldingi turgan stem small_stemni ichida bormi yuqmi
                        '''
                        if i <= 2:  # i==2 bulsa 0 va 1 belgini oladi, [:2] da 2 ikkini uzi kirmaydi
                            if word[:i].casefold() in self.__small_stems:
                                item['stem'], item['lemma'], item['affixed'] = word[:i], word[:i], word[i:]
                                result_items.append(item)

                                # agar len(stem)<=2 bulsa-yu, lekin smal_stem ichidan topilmasa, u xolda stemni uzunligini oshirishi uchun bu yerdan tuliq chiqib ketishi kerak
                                ###break
                        '''

                        # 2.2-rule confidence past bulgan suzlarni exception_words dan qaraydi.
                        # exwords da faqat affix bn tugaydigan suzlar turadi.
                        # agar suz exwordda bulsa qirqmaydi va shu exword yonidagi alternativini qaraydi,
                        # aks holda yani suz exwordda bulmasa qirqib tashlaydi

                        #if float(item["confidence"]) <= 0.1 and False:
                        if False:
                            # print("affix "+item['affix'])
                            # 3-rule
                            # if word in [ambg_stem['stem'] for ambg_stem in self.__ambiguity_stems]:
                            #    return word
                            # 4-rule
                            stem_ex, result = stem_find_exceptions(self, word, i)
                            # print(stem_ex+" "+str(result))
                            if result:
                                return stem_ex
                            else:
                                break  # confidence past bulgan qushimchasi bn borib ex_stemni qidiradi, buni ichida bundin stem bulmasa qirqmay utib ketadi

                        # affiks fayldan qirqiladigan affiks topildi, lekin buni qirqmasdan oldin tekshiramiz, agar qirqilganidan sung 2 ta belgi qoladigan bulsa qirqmasdan utirib yuboramiz, yuqorida kichik stemlar faylidan 2 yo undan kam stem bomi dab qidirvadik, lekin so‘ng dagi suz uchun so degani yuq, lekin,so‘ ni qoldirib ng ni qirqyapti, bunda ‘ belgi bn 3 ta bulyapti, ‘ ni uchirganda 2 belgi qolganda xam bazadan yuqligini bildiradi, va qirqtirmimiz
                        if len(word[:i].replace('‘', '')) <= 2:
                            continue

                        # chiq suzi uchun -ar qushimchasi mavjud, bu yugurar/ishlar dagi -(a)r qushimchasi emas, yani chiqar... kabi suzlardagi -ar qushimchasi faqat chiq suzidan keyin keladi, shuni uchun bundan oldin chiq suzi kelganligini tekshiramiz
                        ''' (-ar qushimchasi istak maylidagi tushar suzlarida xam keladi)
                        if item["affix"].startswith("ar"):
                            if word[:i].casefold() != "chiq":
                                continue
                        '''
                        # print(item)
                        # print(item["affix"].startswith("ar"))
                        # xech qayerdan muammo bulmay, csv fayllarga xam tushmasdan, shu yerga keldi, yani affixes ruyhatdan topildi va resultga qushamiz
                        item['stem'], item['lemma'], item['affixed'] = word[:i], word[:i], word[i:]
                        result_items1.append(item)
                        ###return item  # chopping with 100% confidence

                if result_items1:  # if not empty
                    return result_items1  # agar bir harfni uchirib qolganlarini qushincha deb faraz qilib, affixes listdan qidirib topgan bulsa, buldi, hsuni chiqaradi, yana bir harfni qirqib tekshirib utirmaymiz

            # agar __processing metod ichidagi qadamlardan xech birida bu suz/affix topilmagan bulsagina bu yerda xech nima qirqaolmay uzini chiqarishimiz kerak, agar oldingi steplarda topilgan bulsa buni chiqarmaymiz
            if not res_exist:
                return [{'stem': word, 'lemma': word, 'affixed': '', 'pos': "Undefined"}]

            return [] # agar xech nima topmasa va qirqmasa bush list qaytaramiz, chunki bu bush list boshqa listga qushiladi
        # end of stem_find

        # algorithm for stem
        result_items = [] # barcha variantlarni (item) larni topib shu listga qushib chiqamiz, stem va lemmatize da birinchisini qaytaramiz, analyse da xammasini qaytaramiz

        # 1-step: check non affixed words list
        non_affixed_stems_temp = self.__non_affixed_stems
        for na_stem in non_affixed_stems_temp: #stem,pos,affixed
            if word.casefold() == na_stem['stem'].casefold():
                na_stem['lemma'] = word #bu maydon qushiladi
                na_stem['affixed'] = '' # bu maydon qushiladi
                result_items.append(na_stem)
                return result_items  # result qilib shuni qaytaramiz, boshqa tekshirib utirmaydi

        # agar affix sast bn boshlansa u holda uni asosi ko'r ekanligini tekshirish kerak. yani bu stepni urniga
        # 2-step sat faqat ko'rsat bulganda qirqiladi (so'zni boshi ko'rsat ga teng bulganda)
        affixes_temp = affixes
        if word[:7].casefold() == "ko‘rsat":
            found = False
            for i_affixes in affixes_temp:  # agar kursat topilsa, undan qolgan qushimchani affixes dan qidirib topib, undagi malumotlarni olamiz
                if word[7:] in i_affixes["allomorphs"]:
                    i_affixes['stem'], i_affixes['lemma'], i_affixes['affixed'] = word[:4], word[:4], word[4:]  # bu dictga kursat felini nisbati haqidagi informatsiyani qushib yuborsa xam buladi
                    result_items.append(i_affixes)
                    found = True
            if not found:
                result_items.append({'stem': word[:4], 'lemma': word[:4], 'affixed': word[4:], 'pos': self.POS.VERB})
            return result_items  # result qilib shuni qaytaramiz, boshqa tekshirib utirmaydi

        # 3-step number listdan tekshirish
        affixes_temp = affixes
        for item_number in self.__number_stems:  # agar number.csv dan topilsa, undan qolgan qushimchani affixes dan qidirib topib, undagi malumotlarni olamiz
            if word.casefold().startswith(item_number):
                lemma = item_number
                if word[0].isupper():
                    lemma = lemma.capitalize()
                full_affix = word[len(item_number):]  # [-n:] bunda suzdagi qolganlar harflarni oxirigacha olamiz

                # 1. sonda quhsimcha bulsa qushimchani ruyhatdan qaridi, bulsa resultga qushadi
                found = False
                for i_affixes in affixes_temp:  # qushimchani affixes dan qidirib topib, undagi malumotlarni olamiz
                    if full_affix in i_affixes["allomorphs"] and i_affixes['pos'] == self.POS.NUM:
                        i_affixes['stem'], i_affixes['lemma'], i_affixes['affixed'] = lemma, lemma, full_affix
                        result_items.append(i_affixes)
                        found = True

                #2. agar suz tochni numberdagi suzni uziga teng bulsa, yani qushimchasi yuq bulsa unda buni resultga qushamiz
                if word.casefold() == item_number:
                    result_items.append({'stem': word, 'lemma': word, 'affixed': '', 'pos': self.POS.NUM})
                    found = True
                if found:
                    return result_items  # result qilib shuni qaytaramiz, boshqa tekshirib utirmaydi

        # 4-step exception_stem listdan tekshirish
        affixes_temp = affixes
        for item_ex in ex_stem_list:  # agar exception_stem list dan topilsa, undan qolgan qushimchani affixes dan qidirib topib, undagi malumotlarni olamiz
            if word.casefold().startswith(item_ex['stem']):
                stem = item_ex['stem']
                if word[0].isupper():
                    stem = stem.capitalize()
                full_affix = word[len(stem):]  # [-n:] bunda suzdagi qolganlar harflarni oxirigacha olamiz

                # 1. exception listda quhsimcha bulsa qushimchani ruyhatdan qaridi, bulsa resultga qushadi
                for i_affixes in affixes_temp:  # qushimchani affixes dan qidirib topib, undagi malumotlarni olamiz
                    if full_affix in i_affixes["allomorphs"] and i_affixes['pos'] == item_ex['pos']:
                        i_affixes['stem'], i_affixes['lemma'], i_affixes['affixed'], i_affixes['note'] = stem, stem, full_affix, item_ex['note']
                        result_items.append(i_affixes)

                #2. agar suzni tochni uzi exceptiondagi suzni uziga teng bulsa, yani qushimchasi yuq bulsa unda buni resultga qushamiz
                if word.casefold() == item_ex['stem']:
                    result_items.append({'stem': word, 'lemma': word, 'affixed': '', 'pos': item_ex['pos'], 'note': item_ex['note']})

        # bundan keyin resultni qaytarib yubormaymiz, yana bunga taluqlilari bulishi mumkin, ularni pastda yana tekshirib resultga qushib keyin chiqaramiz

        # 5-step
        affixes_temp = affixes
        if is_lemmatize: # bu yerga lemmatize va analyze dan kelganda kiradi
            for item_lemma in self.__lemma_map:  # agar exception.csv dan topilsa, undan qolgan qushimchani affixes dan qidirib topib, undagi malumotlarni olamiz
                if word.casefold().startswith(item_lemma['word']):
                    lemma = item_lemma['lemma']
                    if word[0].isupper():
                        lemma = lemma.capitalize()

                    full_affix = item_lemma['affix'] + word[len(item_lemma['word']):]  # [-n:] bunda suzdagi qolganlar harflarni oxirigacha olamiz

                    found = False
                    for i_affixes in affixes_temp:  # qushimchani affixes dan qidirib topib, undagi malumotlarni olamiz
                        if full_affix in i_affixes["allomorphs"]:
                            i_affixes['stem'], i_affixes['lemma'], i_affixes['affixed'] = lemma, lemma, full_affix
                            result_items.append(i_affixes)
                            found = True
                    if found:
                        return result_items  # result qilib shuni qaytaramiz, boshqa tekshirib utirmaydi

        # enf of is_lemmatize
        # last step find stem by affix checking from affixes list
        # oxirgi qadam suzni bitta harfdan tashqari xammasini qushimcha deb qarab, affixes listdan qidirib, yana bir xarfni uchirib qidirib topib chiqadi
        result_exist = False
        if result_items:
            result_exist = True

        result_items = result_items + stem_find(self, word, pos, 1, result_exist)  # stem_find() ni ichidan topib yasalgan listni bundan oldingi qadamlarda yasalgan list ustiga qushamiz, qaysidir birlari bush buladi katta ehtimo l bilan


        # if len(stem)<=2:    #checking the small stem is exist or not
        #    if not stem in self.__small_stems:
        #        stem=stem_find(self, word, 3)

        #check stem after chopped affixs, if it should be change, corrected it as lemma, for example: [qiyinchilig+i ->qiyinchilik (xarf uzgarishi)], [avzoy+im->avzo, (xarf ortishi)]
        # if is_lemmatize:
        #     result = self.__correction_stem_lemma(self, result_items)
        return result_items
        # end of processing

    def __clean_word(self, word: str):  # correct form [’]-a’zo, [‘]-o‘,g‘
        if word.isalpha(): # faqat harflardan iborat bulsa, yani apostrof bulmasa
            return word

        word = word.split()[0]  # if word has space take first word

        word = word.replace("g'", "g‘")
        word = word.replace("o'", "o‘")
        word = word.replace("g`", "g‘")
        word = word.replace("o`", "o‘")
        word = word.replace("g’", "g‘")
        word = word.replace("o’", "o‘")
        word = word.replace("gʻ", "g‘")
        word = word.replace("oʻ", "o‘")

        word = word.replace("G'", "G‘")
        word = word.replace("O'", "O‘")
        word = word.replace("G`", "G‘")
        word = word.replace("O`", "O‘")
        word = word.replace("G’", "G‘")
        word = word.replace("O’", "O‘")
        word = word.replace("Gʻ", "G‘")
        word = word.replace("Oʻ", "O‘")

        word = word.replace("'", "’")  # boshqa belgilarni ъ ni kodiga utirish
        word = word.replace("ʼ", "’")  # boshqa belgilarni ъ ni kodiga utirish
        # word = word.replace("’", "’")  # boshqa belgilarni ъ ni kodiga utirish
        return word

    def stem(self, word: str):
        list_item = self.__processing(self.__clean_word(word))
        #print(list_item)
        # return str([d['stem'] for d in list_item])

        # return list_item[0]['stem']    # dict['stem] == dict.get('stem')
        return list_item[0]['stem']

    def lemmatize(self, word: str, pos: str = None):
        # print(self.__lemma_map)
        list_item = self.__processing(self.__clean_word(word), pos, is_lemmatize=True)
        # print(list_item)
        # return {'lemma': list_item[0]['stem'], 'pos': list_item[0]['pos']}  # .['stem'] ['pos']

        # return list_item[0]['lemma']  # .get('stem')
        return list_item[0]['lemma']

    def analyze(self, word: str, pos: str = None):
        # morpheme, bound morpheme [maktablar, maktab=morphem, lar=bound morphem]
        list_item = self.__processing(self.__clean_word(word), pos, is_lemmatize=True, multi_item=True)
        # print(list_item)
        res_list_item = []
        for item in list_item:
            res_dict = {'word': word, 'stem': item['stem'], 'lemma': item['lemma'], 'pos': item['pos']}

            for key in ['id', 'affix','affixed','tense','person','possession','cases','verb_voice1','verb_voice2','verb_voice3','verb_func','impulsion']:   # 'id', 'note', impulsion=mayl, copula=boglama
                if key in item:
                    if item[key] != "":
                        res_dict[key] = item[key]

            for key in ['copula','singular','plural','question','negative']:   # 'id', 'note', impulsion=mayl, copula=boglama
                if key in item:
                    if item[key] != "":
                        res_dict[key] = True
            res_list_item.append(res_dict)

        # genetive case - qaratqich kelishigi
        # Accusative -tushum
        # Dative - jo'nalish
        # Ablative - chiqish
        # Locative o'rin payt

        #  Parse(word='benim', lemma='ben', pos='Noun', morphemes=['Noun', 'A3sg', 'P1sg'], formatted='[ben:Noun] ben:Noun+A3sg+im:P1sg')
        return res_list_item
        # {'affix': 'larni', 'pos': '', 'tense': '', 'person': '', 'cases': 'Tushum', 'singular': '', 'plural': '1', 'question': '', 'negative': '',
        # 'lexical_affixes': '', 'syntactical_affixes': '', 'stem': 'maktab', 'affixed': 'larni'}

    def morph_info(self, word: str, pos: str = None):
        # morpheme, bound morpheme [maktablar, maktab=morphem, lar=bound morphem]
        list_item = self.__processing(self.__clean_word(word), pos, is_lemmatize=True, multi_item=True)
        info = ""
        for item in list_item:
            for key in ['tense','person','possession','cases','verb_voice1','verb_voice2','verb_voice3','verb_func','impulsion']:   # impulsion=mayl, copula=boglama
                if key in item:
                    if item[key] != "":
                        if info != "":
                            info += "|"
                        info += key + "=" + item[key]

            for key in ['copula','singular','plural','question','negative']:   # impulsion=mayl, copula=boglama
                if key in item:
                    if item[key] != "":
                        if info != "":
                            info += "|"
                        info += key + "=True"

            return info  # faqat 0-chi itemni olamiz


    # future methods for dividing into morhpemes
    # def morphemes(self, word: str, pos: str = None):
    #     # preprocessing       ['pre', 'process', 'ing']
    #     # https://github.com/aboSamoor/polyglot/blob/master/notebooks/MorphologicalAnalysis.ipynb
    #     pass

    class POS:
        NOUN = "NOUN"  # Noun
        VERB = "VERB"  # Verb
        ADJ = "ADJ"  # Adjective
        NUM = "NUM"  # Numeric
        ADV = "ADV"  # Adverb
        PRN = "PRN"  # Pronoun

    def pos(self):
        return (
            {'pos': self.POS.NOUN, 'def': 'Noun'},
            {'pos': self.POS.VERB, 'def': 'Verb'},
            {'pos': self.POS.ADJ, 'def': 'Adjective'},
            {'pos': self.POS.NUM, 'def': 'Number'},
            {'pos': self.POS.ADV, 'def': 'Adverb'},
            {'pos': self.POS.PRN, 'def': 'Pronoun'}
        )

    # shu yuqoridagi funksiyalarni yozamiz, pastdagilar esa keyinroq
    # def normalize(self, text: str):
    #     # normalize text is making stemming and lemmatization
    #     # Mening maktabim senikidan chiroyliroq -> men maktab sen chiroyli
    #     return "word"

    # def word_tokenize(self, text):
    #     tokens = []
    #     return tokens

    # def sent_tokenize(self, text):
    #     tokens = []
    #     return tokens

# import time
# start_time = time.time()

# obj = UzMorphAnalyser()

# # sent = "olmasi taqgandim olma taqdimmi kurs kursi gacha namuna ko'plab ular bular sizlar kuchli shanba yuztagacha yuztaga kursi eksport eksportidan masjid masjidi tuman tumani tumanimizni taqdim taqdimi barmoqi barmoq muzqaymoq"
'''
with open(os.path.join(os.path.dirname(__file__) + "/" + "test.txt"), 'r', encoding='utf8') as file:
    sent1 = file.read().rstrip()
sent1 = sent1.replace('	', ' ')
sent1 = sent1.replace('!', ' ')
sent1 = sent1.replace('?', ' ')
sent1 = sent1.replace('“', ' ')
sent1 = sent1.replace('”', ' ')
sent1 = sent1.replace(',', ' ')
sent1 = sent1.replace('.', ' ')
sent1 = sent1.replace('\n', ' ')
sent1 = sent1.replace('(', ' ')
sent1 = sent1.replace(')', ' ')

for token in sent1.split(" "):
    token = token.lower()
    if token == "":
        continue
    print(token + '\t' + obj.stem(token) + '\t' + obj.lemmatize(token) + '\t' + str(obj.analyze(token)))
print("--- %s seconds ---" % (time.time() - start_time))
'''
# with open(os.path.join(os.path.dirname(__file__) + "/" + "test_token.txt"), 'r', encoding='utf8') as file:
#     for token in file:
#         token = token.rstrip()
#         # print(token + '\t' + obj.stem(token) + '\t' + obj.lemmatize(token) + '\t' + str(obj.analyze(token)))
# print("--- %s seconds ---" % (time.time() - start_time))

'''
while (True):
    s = input('word pos =')#.lower()
    s1 = s.split()
    s = s1[0]
    if len(s1)>1:
        p = s1[1]
    else:
        p = None
    # p = input('pos=')

    #print(s + '\t' + obj.stem(s) + '\t' + obj.lemmatize(s) + '\t' + str(obj.analyze(s)))
    print(obj.stem(s))
    print(obj.lemmatize(s, p))
    res_analyze = obj.analyze(s, p)
    for i in res_analyze:
        print(i)
    print(obj.morph_info(s, p))
'''
# print(analyzer.lemmatize('benim'))
# [('benim', ['ben'])]

# print(analyzer.analyze('benim'))
# Parse(word='benim', lemma='ben', pos='Noun', morphemes=['Noun', 'A3sg', 'P1sg'], formatted='[ben:Noun] ben:Noun+A3sg+im:P1sg')
# Parse(word='benim', lemma='ben', pos='Pron', morphemes=['Pron', 'A1sg', 'Gen'], formatted='[ben:Pron,Pers] ben:Pron+A1sg+im:Gen')
# Parse(word='benim', lemma='ben', pos='Verb', morphemes=['Noun', 'A3sg', 'Zero', 'Verb', 'Pres', 'A1sg'], formatted='[ben:Noun] ben:Noun+A3sg|Zero→Verb+Pres+im:A1sg')
# Parse(word='benim', lemma='ben', pos='Verb', morphemes=['Pron', 'A1sg', 'Zero', 'Verb', 'Pres', 'A1sg'], formatted='[ben:Pron,Pers] ben:Pron+A1sg|Zero→Verb+Pres+im:A1sg')

# (s)i opasi kitobi larda yi varianti xam bor, avzoyi, obro'yi (S)i shaklida olsak, bunda S{s,y} buladi. Manba:https://lex.uz/docs/-1625271

# tovush uzgarishlarini lemmatize ga kiritish

'''
Zeyrek's morphological analyzer returns instances of Parse object (based on pymorphy2's Parse), which is a wrapper of namedtuple class.
Parse object fields include:
 word: the word itself
 lemma: base form of the word, as found in a dictionary
 pos: part of speech of the word. Note: Turkish is an agglutinative language, which makes it quite different from widespread European languages. A word can usually be much longer, made of Inflection Groups (IG), which can correspond to words in other languages. Each of these IGs can have its own part of speech, and the part of speech of the word as a whole is determined by the part of speech of the last IG.
 morphemes: sequence of morphemes in the word, a list of strings - abbreviations of English names of morphemes.
 formatted: a human-readable string representation of the analysis. There are several kinds of possible formats. Default formatter shows the dictionary item and its part of speech, and morphemes (with their surfaces, if available), divided into inflectional groups by | character.
'''

#(i)t kirit, (i)l ko'ril, (i)n ko'rin, Y{bora,kuylay}, (a)r{borar,kuylar} qo'shimchalarini uchiramiz bazadan, chunki bir xarfli qushimchalar suzlarni oxirini kup qirqib yuboradi

# test file statistics:
# source:daryo.uz, category:4, documents for each category: 10
# 5,288 unique words of 11,952 total (44.24%):