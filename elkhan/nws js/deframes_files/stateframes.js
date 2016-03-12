/* ======================================================================
DESC: javascript common to all state frameset files in the NAWRS site.

PLATFORMS: all client side systems using browsers which accept Javascript 1.3
====================================================================== */

     MaxIndex = 30;
     SiteArray = new Array(MaxIndex);
     SelectedIndex = 0;
     usrMode = "nolist";
     listMode = false;
     listWindow = window.open("listframes.html", "ProductList", "width=600,height=500,resizable=yes");
     listOpen = true;
     openCount = 0;
     listRequest = false;
     deleteList = false;
     USMapRequest = false;
     requestSubmit = false;
     editWindow = null;
     editOpen = false;
    productsWindow = null;
    productsOpen = false;
    cookieRestored = true;
    browser = "";
    Netscape = true;
    oneDay = 24 * 60 * 60 * 1000;
    fiveDays = oneDay * 5;
    thirtyDays = oneDay * 30;
     
     function InitRestoreOff()  {
      var value;
      browser = navigator.appName;
      if (browser.substring(0, 8) == "Netscape")
        Netscape = true;
      else Netscape = false;
      value = (getCookie("USERMODE"));
      if (value == null)  {   // can we get a user mode?
        usrMode = "nolist";   // no, set user to "one-click" mode
        saveCookie("USERMODE", usrMode); // and save it
        }
      else   // yes
        usrMode = value;   //   restore user mode
      if (getCookie("SELECTEDINDEX") != null)  {  // is the SelectedIndex accessable?
        cookieRestored = false;  // yes, set the internal flag
        usrMode = "list";   // set user to "list" mode
        }
      if (usrMode == "list")   { // are we in "List" mode?
        listMode = true;   // yes, set flag for list mode
        frames[0].document.location = "banner.html";
        saveCookie("USERMODE", usrMode);
        frames[1].StatusLocked(0);  // make sure we can display status
		if (!cookieRestored)	// did we have a list cookie?
        	frames[1].StatusBar(-1, "List has not been restored!!");	// yes
      if (!listWindow.closed) { // is the list window open?
		   listWindow.frames[0].document.location = "listbanner.html"; // yes
		   listWindow.frames[1].document.location = "listonlinehelp.html";
         }
      }
      else   {
        listMode = false;
        frames[0].document.location = "scbanner.html";
        }
      }
     
     // Convert to "List" mode
     function MakeList()   {
       usrMode = "list";
       saveCookie("USERMODE", usrMode);
       listMode = true;   // set flag for list mode
       frames[0].document.location = "banner.html";
		 listWindow.frames[0].document.location = "listbanner.html";
		 listWindow.frames[1].document.location = "listonlinehelp.html";
       }
		 
	  // Convert to "Single-Click" mode 
	  function SingleClick()	{
       usrMode = "nolist";
       saveCookie("USERMODE", usrMode);
       listMode = false;   // set flag for "single-click" mode
       frames[0].document.location = "scbanner.html";
		 listWindow.frames[0].document.location = "sclistbanner.html";
		 listWindow.frames[1].document.location = "sclistonlinehelp.html";
		 deleteCookie("SELECTEDINDEX");	// yes, delete existing
		 deleteCookie("STATEFRAME");	// "list mode" cookies
		 deleteCookie("SITEARRAY");
		 }
     
     function fetchEntry(index)  {
       return SiteArray[index]
       }
       
     function saveEntry(index, entry)  {
       SiteArray[index] = entry
       }
     
     function saveIndex(index)  {
       SelectedIndex = index;
       }
     
    // Return true if entry found and deleted
     function DeleteEntry(entry)  {
        var i = 0, j;
        while (i < SelectedIndex)  {
          if (entry == SiteArray[i])  {
            frames[1].StatusLocked(0);
            frames[1].StatusBar(-1, entry, "Deleted: ");
            frames[1].StatusLocked(5);
            SiteArray[SelectedIndex] = "";
            for (j = i; j < SelectedIndex; ++j)  {
              SiteArray[j] = SiteArray[j + 1];
              }
            if (--SelectedIndex == 0)
              ToggleButton(0, "request.gif");
            return true;
            }
          ++i;
          }       
        return false;
       }
       
    function DoubleClick(entry)  {
        var i = 0, j;
        while (i < SelectedIndex)  {
          if (entry == SiteArray[i])  {
          SubmitForm();
            return true;
            }
          ++i;
          }       
        return false;
      }

     function listRequestFalse()  {
       listRequest = false;
       }
       
     function setDeleteList(condition)  {
	  	if (condition == null)
       deleteList = true;
		else deleteList = condition;
       }

     function WriteForm()  {
       var i;
       if (!listOpen && listRequest)
         listWindow = window.open("listframes.html", "ProductList", "width=640,height=480,resizable=yes");
       if (listOpen)  {
         listRequest = false;  // reset request flag         
         listWindow.frames[2].document.open("text/html");
         listWindow.frames[2].document.writeln('<BODY ONFOCUS="parent.FocusCheck()"><FORM METHOD="GET" NAME="ProductRequest" TARGET="Products" ACTION="http://weather.noaa.gov/cgi-bin/mzonedata.pl">');
         listWindow.frames[2].document.writeln('<P><INPUT TYPE="HIDDEN" NAME="RequestSites" VALUE="Request Products"><TEXTAREA NAME="Sites" ROWS="30" COLS="125" WRAP="Off">');
         for (i = 0; i < SelectedIndex; ++i)  {
          listWindow.frames[2].document.writeln(SiteArray[i]);
          }
        listWindow.frames[2].document.writeln("</TEXTAREA></P></FORM></BODY>");
        listWindow.frames[2].document.close();
        }
       }
       
     function RequestSubmit(flag)  {
       requestSubmit = flag;
       }
       
     function SubmitForm()  {
       if (listOpen)  // is List Window already open?
         listWindow.SubmitForm();  // yes
       else  {  // no
         requestSubmit = true;  // set the product request flag
         ShowList();  // open List Window
         OpenProducts(); // and Product Window
         }
       }
              
     function ShowList()  {  // display the List Window
       if (listOpen)  {  // is List Window already open?
         listWindow.frames[2].focus();  // yes, give it focus
         }
       else  {  // no, we must open it
        listRequest = true;
        WriteForm();
         }
       }
   
  function DeleteEntries()  {  // display the Delete Entries Window
    editOpen = true;
    editWindow = window.open("editframes.html", "EditList", "width=640,height=480,resizable=yes")
    }
    
   function ClearStrings()  {
     SelectedIndex = 0;
     SiteArray[0] = "";
    WriteForm();
      frames[1].StatusLocked(0);
      if (listMode)  // are we in List mode?
         frames[1].StatusBar(-1, "List of Requested Products Has Been Cleared"); // yes
      else  // no
         frames[1].StatusBar(-1, "Requested Product Has Been Cleared");
      frames[1].StatusLocked(5);
		if (listMode)  // are we in "List Mode"?
      	ToggleButton(0, "request.gif");  // yes
     }
     
	 function deleteCookie(name)	{
      var expDate = new Date();
		expDate.setTime(expDate.getTime() - fiveDays);
	 	document.cookie = name + "=value; expires=" + expDate.toGMTString();
	 	}
     
    function saveCookie(name, value)  {
      //var expDate = new Date()
      // set 30 day expiration date
      //expDate.setTime(expDate.getTime() + thirtyDays)
      //document.cookie = name + "=" + escape(value) + "; expires=" + expDate.toGMTString()
      document.cookie = name + "=" + escape(value);   //session cookie
      }
      
    function saveState()  {
      var i, arrayString = "", numberString;
      if (SelectedIndex > 0)  {
        saveCookie("STATEFRAME", document.location);
        saveCookie("SELECTEDINDEX", SelectedIndex.toString());
        for (i = 0; i < SelectedIndex; ++i)  {
          numberString = '[' + i.toString() + ']';
          arrayString = arrayString + numberString + SiteArray[i];
          }
        saveCookie("SITEARRAY", arrayString);
        frames[1].StatusBar(-1, "Current List has been saved:  " + SelectedIndex.toString() + " entries");
        }
      }
    
    function getCookie(name)  {
      var result = null;
      var cookieString = " " + document.cookie + ";";
      var searchName = " " + name + "=";
      var start = cookieString.indexOf(searchName);
      var end;
      if (start != -1)  {
        start += searchName.length;  // get past name
        end = cookieString.indexOf(";", start);
        result = unescape(cookieString.substring(start, end));
        }
      return result;
      }
      
    function getState()  {
      var value, arrayString, indexString, i;
      var start, end = 0;
      if (requestSubmit)  // did we just submit the List form?
        return;  // yes, we shouldn't restore anything
      CookieRestored();  // make sure cookie restored flag is on
      value = getCookie("SELECTEDINDEX");
      if (value != null)  {  // did we get the cookie?
        SelectedIndex = parseInt(value);  // yes
        if (SelectedIndex > 0)  {  // do we have any array entries?          
          arrayString = getCookie("SITEARRAY");  // yes
          if (arrayString != null)  {  // did we get the array?
            ToggleButton(0, "request1st.gif");  // yes
            for (i = 0; end < arrayString.length; ++i)  {
              indexString = '[' + i.toString() + ']';
              end = arrayString.indexOf(indexString);
              if (end == -1)  // did we get the next entry?
                break  // no, done
              start = arrayString.indexOf(']', end);
              end = arrayString.indexOf('[', ++start);
              if (end == -1)  // is this the last entry?
                end = arrayString.length;  // yes
              SiteArray[i] = arrayString.substring(start, end);
              }
            if (listOpen)
              WriteForm();
            frames[1].StatusLocked(0);  // make sure we can display status
            frames[1].StatusBar(-1, "List has been restored:  " + SelectedIndex.toString() + " entries");
            }
          else SelectedIndex = 0;  // we did not get an array
          }
        }
      else  {  // we did not get a cookie entry
        frames[1].StatusLocked(0);  // make sure we can display status
        frames[1].StatusBar(-1, "Cookie is not accessible:  List cannot be restored!");
        if (listOpen)  // is List window open?
          WriteForm();  // yes
        }
      }
      
    function CookieRestored()  {      
        frames[0].document.images[11].src = "restore.gif";  // normal restore button
        cookieRestored = true;  // reset the flag
      }
 
    function ToggleButton(index, image)   {
       frames[0].document.images[index].src = image;
       }
    
    function ListOpen()  {
      listOpen = true;
      return ++openCount;
      }
      
    function ListClose()  {
      if (listOpen)  
        listOpen = false;
      }
      
    function EditOpen()  {
      editOpen = true;
      }
      
    function EditClose()   {
       if (editOpen)
          editOpen = false;
       }
       
    function OpenProducts()  {  // open the "Products" window
      if (!productsOpen)  {  // is Product window open?
        productsWindow = window.open("productframes.html", "ProductFrames", "width=700,height=480,toolbar=yes,resizable=yes");  // no, open it
        return true;
        }
      else return false;
      }
      
    function ProductsOpen(flag)  {
      productsOpen = flag;
      }

    function InitProducts()  {
      productsWindow.InitProducts();
      }

     function FocusCheck()  {
       if (editOpen)  {  // did user leave Delete window open?
         editWindow.EditRequestClose();  // yes, request close
         editWindow.focus();  // complete the request
        if (USMapRequest)
          USMap();
        }
       }
     
     function USMapExit()  {
       USMapRequest = true;
       }
     
     function USMap()  {
       var path, index, separator, index1;
       if (Netscape)
         separator = "/";
       else  separator = "\\";
      path = window.location.pathname;
      if (path.indexOf(".html") != -1)  // does path end in a file?
        {  // yes
        index = path.lastIndexOf(separator);
        if (separator == "\\")  {  // is browser IE?
          index1 = path.lastIndexOf("/");  // yes
          if (index1 > index)
            index = index1;
          }
        window.location.pathname = path.substring(0, index + 1) + "usframes.html";
        }
      else  // path needs the final new file
        window.location.pathname = path.substring(0, path.length) + separator + "usframes.html";
       }
       
     function TopTarget(url)  {
    window.location.href = url;
       }
     
     function MainHelp()  {  
     var helpWindow;
	  if (listMode)  // are we in "List Mode"
        helpWindow = window.open("mainhelp.html", "MainHelp", "width=425,height=450,scrollbars,resizable");  // yes
	  else helpWindow = window.open("scmainhelp.html", "SCMainHelp", "width=425,height=450,scrollbars,resizable");
        }
        
    function Exit()  {
      FocusCheck();  // make sure Edit window closed
      if (listOpen)  {  // Did user close this window?
        listWindow.MainClose();  // yes, set flag and
        listWindow.close();  // close List window
        }
      if (productsOpen)  {  // is the Products window open?
        if (productsWindow.mainWindow)
          productsWindow.MainWindow(false);
        productsWindow.close();  // yes
        }
      }  
