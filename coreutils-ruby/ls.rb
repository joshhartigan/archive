#!/usr/bin/ruby

def usage
  puts 'Usage:'
  puts '  `ls -a`:'
  puts '    List the files including hidden files in the'
  puts '    current directory.'
  puts '  `ls`:'
  puts '    List the files in the current directory.'
  exit
end

if ARGV == []
  Dir.glob('*').each do |file|
    puts file
  end

elsif ARGV[0] == '-h'
  usage

elsif ARGV[0] == '-a'
  Dir.entries('.').each do |file|
    puts file
  end

else ARGV[0] != '-a'
  Dir.glob( ARGV[0] + '/*' ).each do |file|
    puts file
  end

end

