import sys
from clang.cindex import Index, SourceLocation, Cursor, File, CursorKind, TypeKind, Config, LibclangError

def getQuickFix(diagnostic):
  # Some diagnostics have no file, e.g. "too many errors emitted, stopping now"

  if diagnostic.location.file:
    filename = diagnostic.location.file.name
  else:
    filename = ""

  if diagnostic.severity == diagnostic.Ignored:
    type = 'I'
  elif diagnostic.severity == diagnostic.Note:
    type = 'I'
  elif diagnostic.severity == diagnostic.Warning:
    type = 'W'
  elif diagnostic.severity == diagnostic.Error:
    type = 'E'
  elif diagnostic.severity == diagnostic.Fatal:
    type = 'E'
  else:
    return None

  res =  dict({ 'buf' :  filename,
    'lnum' : diagnostic.location.line,
    'col' : diagnostic.location.column,
    'text' : diagnostic.spelling,
    'type' : type})
  return res

def getQuickFixList(tu):
  return filter (None, map (getQuickFix, tu.diagnostics))

def init():
  conf = Config()

  # here we use the libclang.dylib from the vim plugin -- YouCompleteMe


  # path = "/Users/lono/.config/nvim/plugged/YouCompleteMe/third_party/ycmd"
  # path = "/Applications/Xcode.app/Contents/Frameworks"
  path = "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib"
  # path = "/Library/Developer/CommandLineTools/usr/lib/"
  # path = "/Applications/Xcode8.app/Contents/Frameworks"
  Config.set_library_path(path)
  conf.set_library_path(path)
  try:
    conf.get_cindex_library()
  except LibclangError as e:
    print "Error: " + str(e)

def main():
    init()
    index = Index.create()
    print sys.argv[1]
    arg = [ '-x', 'objective-c',
            '-arch', 'arm64',
            '-fmodules',
            # '-D__IPHONE_OS_VERSION_MIN_REQUIRED=80000',
            # '-miphoneos-version-min=9.3',
            '-isysroot', '/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk',
            # '-F/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk/System/Library/Frameworks',
            # '-isysroot', '/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk'
           ]
    tu = index.parse(sys.argv[1], args=arg)

    print getQuickFixList(tu)

if __name__ == '__main__':
    main()
