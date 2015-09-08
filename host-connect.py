import paramiko, base64

  
key = paramiko.RSAKey(data=base64.decodestring('AAAAB3NzaC1yc2EAAAADAQABAAABAQDWdYVbjZ/CG7bo4fGxxqAPzy6V/sy2T7vlVnt51HyFEi4Q7vmf3FXct/bxAZAJ0lu3EIC7JwtOF8ecU0T5h10RoZC/8rNDscgMvGjPriQefGv41S2lJy/Wi862kjXSNQqsEFU/wV4MqHtDkEzuAF9riIXwBNSUCTKw3QZcrRqf9geHOdKH4ErpKZ8UAF+gHrhqAs/evN2N3v9GCMP6XBYTvZemtQIv6kutmHProwYva8jjwkXPit4g84LHJqGU3VwP/WrLw8odvN5CsMgChZXat7LT2YCm06+jBBvtmF5dpLQNupUyaZ7wM744IFZNNA05FxeAXGN7oZHD28TO6Cuv'))
client = paramiko.SSHClient()
print client
client.get_host_keys().add('review.coprhd.org', 'ssh-rsa', key)
client.connect('', username='root', password='')
stdin, stdout, stderr = client.exec_command('uname -a')
for line in stdout:
        print '... ' + line.strip('\n')
  
client.close()
