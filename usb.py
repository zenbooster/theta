from common import *

usb_cap = from_brep('./brep/YU-USB3-JSX-01-001.brep').rotateY(deg(-90)).rotateZ(deg(-90)).down(2.2)

def get_usb():
    return usb_cap

if __name__ == "__main__":
	m = get_usb()

	display(m)#, color=(1, 1, 1, 0.5))
	show()
