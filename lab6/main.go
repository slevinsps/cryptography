package main

import (
	"bufio"
	"container/heap"
	"fmt"
	"io/ioutil"
	"os"

	bitstream "github.com/bearmini/bitstream-go"
)

type huffmanTree interface {
	Freq() int
}

type huffmanLeaf struct {
	freq  int
	value byte
}

type huffmanNode struct {
	freq        int
	left, right huffmanTree
}

func (n huffmanLeaf) Freq() int {
	return n.freq
}

func (n huffmanNode) Freq() int {
	return n.freq
}

type treeHeap []huffmanTree

func (th treeHeap) Len() int { return len(th) }
func (th treeHeap) Less(i, j int) bool {
	return th[i].Freq() < th[j].Freq()
}
func (th *treeHeap) Push(ele interface{}) {
	*th = append(*th, ele.(huffmanTree))
}

func (th *treeHeap) Pop() (popped interface{}) {
	popped = (*th)[len(*th)-1]
	*th = (*th)[:len(*th)-1]
	return
}
func (th treeHeap) Swap(i, j int) { th[i], th[j] = th[j], th[i] }

func buildTree(symFreqs map[byte]int) huffmanTree {
	var trees treeHeap
	for c, f := range symFreqs {
		trees = append(trees, huffmanLeaf{f, c})
	}
	heap.Init(&trees)
	for trees.Len() > 1 {
		a := heap.Pop(&trees).(huffmanTree)
		b := heap.Pop(&trees).(huffmanTree)

		heap.Push(&trees, huffmanNode{a.Freq() + b.Freq(), a, b})
	}
	return heap.Pop(&trees).(huffmanTree)
}

func generateCodes(codes map[string]byte, tree huffmanTree, prefix []byte) {
	switch i := tree.(type) {
	case huffmanLeaf:
		codes[string(prefix)] = i.value
	case huffmanNode:
		prefix = append(prefix, '0')
		generateCodes(codes, i.left, prefix)
		prefix = prefix[:len(prefix)-1]

		prefix = append(prefix, '1')
		generateCodes(codes, i.right, prefix)
		prefix = prefix[:len(prefix)-1]
	}
}

func readFromFile(file string) ([]byte, error) {
	data, err := ioutil.ReadFile(file)
	return data, err
}

func writeToFile(data, file string) {
	ioutil.WriteFile(file, []byte(data), 0644)
}

func readline() string {
	bio := bufio.NewReader(os.Stdin)
	line, _, err := bio.ReadLine()
	if err != nil {
		fmt.Println(err)
	}
	return string(line)
}

func main() {
	fmt.Print("Enter file name: ")
	filename := readline()
	text, err := readFromFile(filename)
	if err != nil {
		panic(err)
	}

	fmt.Println("Initial text size: ", len(text)*8)
	sumOfFrequencies := make(map[byte]int)
	for _, c := range text {
		sumOfFrequencies[c]++
	}
	tree := buildTree(sumOfFrequencies)

	codes := map[string]byte{}
	codesReversed := map[byte]string{}
	generateCodes(codes, tree, []byte{})
	for k, v := range codes {
		codesReversed[v] = k
	}

	compressed := ""
	writer, err := os.Create(filename + ".compressed")
	if err != nil {
		panic(err)
	}
	w := bitstream.NewWriter(writer)
	for _, c := range text {
		for b := range codesReversed[c] {
			if codesReversed[c][b] == '0' {
				err = w.WriteBit(0)
			} else {
				err = w.WriteBit(1)
			}
		}
		compressed += codesReversed[c]
	}
	err = w.Flush()

	reader, err := os.Open(filename + ".compressed")
	if err != nil {
		panic(err)
	}

	r := bitstream.NewReader(reader, nil)
	bit, err := r.ReadBit()
	if err != nil {
		panic(err)
	}
	toBeDecompressed := ""
	for err == nil {
		if bit == 0 {
			toBeDecompressed += "0"
		} else {
			toBeDecompressed += "1"
		}
		bit, err = r.ReadBit()
	}
	
	fmt.Println("Compressed size: ", len(toBeDecompressed))
	decompressed := []byte{}
	currentRune := ""
	for _, c := range toBeDecompressed {
		currentRune += string(c)
		if b, ok := codes[currentRune]; ok {
			decompressed = append(decompressed, b)
			currentRune = ""
		}
	}
	decompressed = decompressed[:len(decompressed)-1]
	ioutil.WriteFile(filename+".decompressed", decompressed, 0644)
}
