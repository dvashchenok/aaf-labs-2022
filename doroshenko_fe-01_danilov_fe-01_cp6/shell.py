from run import run

text = ''
while True:
    try:
      text = input('shit_DB > ')
      result, error = run(text)
      if error:
          print(error.as_string())
    except Exception as e:
      print("An error occurred:", e)
      continue
