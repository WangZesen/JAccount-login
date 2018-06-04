import base64

def get_base64(file_name):
	with open(file_name, 'rb') as f:
		base64_data = base64.b64encode(f.read())
		print (base64_data)
		return base64_data


if __name__ == "__main__":
	get_base64('test.jpg')
