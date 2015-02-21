#!/usr/bin/ruby

def usage
  puts 'Usage:'
  puts '  `echo [STRING...]`:'
  puts '    Echo the STRING(s) to standard output'
  puts '  `echo`:'
  puts '    Echo a newline to standard output'
  exit
end

if ARGV == []
  puts
elsif ARGV[0] == '-h'
  usage
else
  puts ARGV.join ' '
end

