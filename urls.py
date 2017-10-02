'''
Created on Sep 30, 2017

@author: root
'''
# urls = ( '/', 'index',
#          '/login', 'webpages.login',
#          '/about', 'webpages.about',
#          '/home', 'webpages.home')
import webpages

urls = ( '/', 'webpages.index',
         '/login', 'webpages.login',
         '/about', 'webpages.about',
         '/home', 'webpages.home',
         '/logout', 'webpages.logout',
         '/safetyinstructions', 'webpages.safetyinstructions')
