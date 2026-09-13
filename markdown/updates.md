---
title: a better way of blocking macOS updates
---
a while ago, I read [rob's amazing article on blocking updates to macOS tahoe](https://robservatory.com/block-the-upgrade-to-tahoe-alerts-and-system-settings-indicator/).  
as great as this is, it(like stated in the article) only works for 90 days, after which you'll have to do it again  
i sent this article to a friend of mine and they showed me a much better way of stopping update notifications    
```
sudo defaults write com.apple.MobileAsset MobileAssetAssetAudience -string 92897351-9c90-4132-84a8-2c4b3b5fced5
sudo defaults write com.apple.MobileAsset MobileAssetServerURL-com.apple.MobileAsset.SoftwareUpdate -string "https://swscan.apple.com/content/catalogs/others/index-seed-26-15-14-13-12-10.16-10.15-10.14-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog.gz"
sudo killall -HUP mobileassetd
sudo killall -HUP betaenrollmentd
```
the way this works is by the update catalog to an invalid value  

if you ever want to update your mac again, 
```
sudo defaults write com.apple.MobileAsset MobileAssetAssetAudience -string 60b55e25-a8ed-4f45-826c-c1495a4ccc65
sudo defaults write com.apple.MobileAsset MobileAssetServerURL-com.apple.MobileAsset.SoftwareUpdate -string "https://swscan.apple.com/content/catalogs/others/index-26-15-14-13-12-10.16-10.15-10.14-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog.gz"
sudo killall -HUP mobileassetd
sudo killall -HUP betaenrollmentd
```
