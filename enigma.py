from typing import List


class Reflector:
    def __init__(self, natStr: str, rotStr: str) -> None:
        self.natList = []
        self.rotList = []
        if len(natStr) != len(rotStr):
            raise ValueError
        for ch in natStr.lower():
            self.natList.append(ch)
        for ch in rotStr.lower():
            self.rotList.append(ch)
        return

    # something wrong
    def getOutput(self, chin: str, reverse: bool = False) -> str:
        if reverse:
            # return self.rotList[self.natList.index(chin)]
            return self.natList[self.rotList.index(chin)]
        else:
            # return self.natList[self.rotList.index(chin)]
            return self.rotList[self.natList.index(chin)]


class Scrambler(Reflector):
    def __init__(self, natStr: str, rotStr: str, offset: str or int = 0) -> None:
        super().__init__(natStr, rotStr)
        self.setOffset(offset)
        return

    def setOffset(self, offset: str or int) -> None:
        if type(offset) is int:
            num = offset % len(self.rotList)
        elif type(offset) is str:
            num = self.natList.index(offset)
        else:
            raise ValueError
        self.cur = num % len(self.rotList)
        for _ in range(num):
            self.rotateRotList()
        return

    def getCur(self) -> int:
        return self.cur

    def getCurAsStr(self) -> str:
        return self.rotList[self.getCur()]

    def rotateRotList(self) -> bool:
        self.cur += 1
        tmp = self.rotList.pop(0)
        self.rotList.append(tmp)
        # tmp = self.natList.pop(0)
        # self.natList.append(tmp)
        # print(self.natList)
        # print(self.rotList)
        if self.cur // len(self.rotList) > 0:
            self.cur %= len(self.rotList)
            return True
        else:
            return False

    # def getOutput(self, chin: str) -> str:
        # return self.natList[self.rotList.index(chin) - self.cur) % len(self.rotList)]


class PlugBoard:
    plugs = {}

    def __init__(self, natural: str, pgs: List[str]) -> None:
        for pg in pgs:
            self.plugs[pg[0]] = pg[1]
            self.plugs[pg[1]] = pg[0]
        for n in natural:
            if n in self.plugs.keys():
                continue
            else:
                self.plugs[n] = n
        return

    def getOutput(self, chin: str) -> str:
        return self.plugs[chin]


class Enigma:
    natural = 'abcdefghijklmnopqrstuvwxyz'
    scs = []
    refl = Reflector(natural, 'YRUHQSLDPXNGOKMIEBFZCWVJAT'.lower())
    pb = PlugBoard(natural, [])
    rotOrder = []

    def __init__(self, natural: str, keys: str, rotOrder: List[int] or None) -> None:
        if rotOrder and len(keys) != len(rotOrder):
            raise ValueError
        self.natural = natural
        self.addScrambler('EKMFLGDQVZNTOWYHXUSPAIBRCJ'.lower(), keys[0])
        self.addScrambler('AJDKSIRUXBLHWTMCQGZNPYFVOE'.lower(), keys[1])
        self.addScrambler('BDFHJLCPRTXVZNYEIWGAKMUSQO'.lower(), keys[2])
        self.addScrambler('uwygadfpvzbeckmthxslrinqoj', -1)
        if rotOrder == None:
            self.rotOrder = [i for i in range(len(self.scs))]
        else:
            self.rotOrder = rotOrder
        return

    def addScrambler(self, rotStr: str, offset: int = 0) -> None:
        self.scs.append(Scrambler(self.natural, rotStr, offset))
        return

    def getCurrentWindow(self) -> str:
        ret = ''
        for rotN in self.rotOrder:
            ret += self.scs[rotN].getCurAsStr()
        return ret

    def rotateScrambler(self) -> None:
        bl = True
        for rotN in self.rotOrder[::-1]:
            if bl:
                bl = self.scs[rotN].rotateRotList()
                continue
            else:
                break
        return

    def getPlainChr(self, ch: str) -> str:
        ret = ch
        self.rotateScrambler()
        ret = self.pb.getOutput(ret)
        print(ret, 'pb')
        for rotN in self.rotOrder[::-1]:
            ret = self.scs[rotN].getOutput(ret)
            print(ret, 'scrambler', rotN, 'pos:', self.scs[rotN].getCur())
        ret = self.refl.getOutput(ret)
        print(ret, 'refl')
        for rotN in self.rotOrder:
            ret = self.scs[rotN].getOutput(ret, True)
            print(ret, 'scrambler', rotN, 'pos:', self.scs[rotN].getCur())
        ret = self.pb.getOutput(ret)
        print(ret, 'pb')
        return ret

    def getPlainText(self, encrypted: str) -> str:
        ret = ''
        for c in encrypted:
            if not c in [i for i in self.natural]:
                ret += c
                continue
            ret += self.getPlainChr(c)
        return ret


if __name__ == '__main__':
    enigma = Enigma('abcdefghijklmnopqrstuvwyxz', 'aaa', [0, 1, 2])
    pln = input()
    print(pln, enigma.getPlainText(pln))
