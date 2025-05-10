class AnimationData:
  name = ""
  begin = 0
  end = 250
  step = 1
  action = ""
  camera = ""

  def set(self, name: str, value: str):
    if name == "begin":
      self.begin = int(value)
    elif name == "end":
      self.end = int(value)
    elif name == "step":
      self.step = int(value)
    elif name == "action":
      self.action = value
    elif name == "camera":
      self.camera = value
    else:
      print(name + " not found.")
  
  def isDefined(self):
    return len(self.name) > 0


# TODO: better format & parsing?
def parse_animation_data(content: str) -> tuple[AnimationData, str]:
  res = AnimationData()
  index = content.find("\n")
  while index >= 0 and not (content.startswith("#") and res.isDefined()):
    line = content[0:index].strip()
    content = content[index+1:].strip()
    if line.startswith("#"):
      res.name = line[1:].strip()
      print("find animation: " + res.name)
    elif line.startswith("* "):
      line = line[2:]
      print("parse property line: " + line)
      eq = line.find("=")
      name = line[0:eq].strip()
      value = line[eq+1:].strip()
      res.set(name, value)
    else:
      print("invalid line: " + line)
    index = content.find("\n")

  line = content
  if line.startswith("* "):
    line = line[2:]
    print("parse property line: " + line)
    eq = line.find("=")
    name = line[0:eq].strip()
    value = line[eq+1:].strip()
    res.set(name, value)
    content = ""

  return res, content.strip()
