#���öȸߵ�д��
def reverse(text):
    return text[::-1]

def is_palindrome(text):
    return text == reverse(text)

something = input('Enter text:')
if (is_palindrome(something)):
    print('Text is palindrome')
else:
    print('Is not palindrome')


#���취
something = input('Enter text:')
turn = something[::-1]
if turn == something:
    print('Y')
else:
    print('N')


#�ɹ��˴�Сд�Ϳո��ϰ�ⷽ��
import string

def reverse(text):
    return text[::-1]

def is_palindrome(text):
    text = text.lower()
    text = text.replace(' ','')
    for char in string.punctuation:
        text = text.replace(char,'')
    return text == reverse(text)

def main():
    something = input('Enter text:')
    if (is_palindrome(something)):
        print("Yes, ��{0}�� is a palindrome".format(something))
    else:
        print("No��,{0}�� is not a palindrome".format(something))

if __name__ == '__main__':
    main()
else:
    print("user_input.py was imported!")