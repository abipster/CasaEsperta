# CasaEsperta - [Organizr](https://organizr.app/)

There's nothing special about the container deploy.

### Configuration
After the initial configuration, you can customize this in many ways. I'll write how I configured my instance.

### Theme and Custom CSS
Personally, I like the Space Gray Theme. To enable it go to Settings -> Customize -> Marketplace and install the theme by clicking on the + icon on its row.

After that, go to Appearance -> Colors & Themes and change the theme to Space_Gray and Style to Dark.

I don't like the behavior of the sidebar. To stop it from showing more on mouse hover, go to Custom CSS tab and write this:

```css
@media only screen and (min-width: 768px) {
  .sidebar:hover .hide-menu {
    display: none;
  }
  .sidebar:hover .sidebar-head,
  .sidebar:hover {
    width: 60px;
  }
}
```
Save and refresh the page.


### Homepage
Then enable the Homepage by going to Settings -> Tab Editor and setting the Homepage item to Active. Now put it in the first place of the list.

If you have Netdata installed and want to display the custom dashboard on Organizr's homepage:

Edit [overview.html](../main_server/docker/netdata/overview.html) to replace example.pt domain with your own. After that copy it to `~/docker/overview.html`, then run this on the server to copy the custom netdata dashboard to Netdata's container:
```
docker cp ~/docker/overview.html netdata:/usr/share/netdata/web/
dexec netdata bash -c 'chown root:root /usr/share/netdata/web/overview.html'
```

I also have 2 [Raspberry Pis](r-pi.md) with Netdata installed and also want their smaller custom dashboard on the Homepage. Edit [overview-pi.html](../main_server/docker/netdata/overview-pi.html) and replace example.pt domain with your own. The pi-data prefix also needs to be changed to what you configured when you reverse-proxied Netdata on the Raspberry Pi. I have pi-data for one and pi2-data for the second. Then,for each Pi copy the respective html to your Pi's home directory and:
```
sudo cp ~/overview-piX.html /usr/share/netdata/web/overview.html
sudo chown netdata:netdata /usr/share/netdata/web/overview.html
```

Now each Pi also have a custom dashboard published at  https://piX-data.example.pt/overview.html.

Going back to Organizr, go to Settings -> Tab Editor -> Homepage Items and enable CUSTOMHTML-1 with User as Minimum Authentication. In the code tab, add the following if you only want the main server's dashboard:
```html
<div style="overflow:hidden;height:900px;width:100%;position: relative;"> 
    <embed style="height:calc(100%);width:calc(100%)" src='https://netdata.example.pt/overview.html' />
</div>
```

If you want the 2 Pi's plus the Server dashboard, edit [organizr_homepage.html](../main_server/docker/netdata/organizr_homepage.html) and replace example.pt domain with your own, the pi-data prefixes to match yours and copy the html to same place of the above instruction.

Save and refresh the page.