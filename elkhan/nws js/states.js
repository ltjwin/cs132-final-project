/* ======================================================================
DESC: javascript common to all state HTML files in the NAWRS site.

PLATFORMS: all client side systems using browsers which accept Javascript 1.3
====================================================================== */
     MaxIndex = 30;
     StatusBarLocked = 0;
     
     // function saveCookies()  {
     //  // StatusBarLocked = 0;  // make sure we can display status
     //  //  parent.saveState();
     //   }
     
     // function restoreCookies()  {
     //   // parent.getState();
     //   }
     
      function DisplaySites(string)   {
	    console.log("DisplaySites function")
      var i, index;
      var zoneString, zoneNbr, preString, postString, totalString, editString;
      var param2;
      zoneString = string.substring(3, 6);
      editString = string.substring(0, 6);
      i = parseInt(zoneString);
      if (isNaN(i))  {  // is this an alpha zone?
        postString = zoneString.substring(2, 3);  // yes
        zoneString = '09' + postString;  // substitue numeric index
        preString = editString.substring(0, 3);
        editString = preString + '00' + postString;
        }
      index = zoneString.indexOf('00');
      if (index != 0)  {  // is this 2 leading zeroes?
        index = zoneString.indexOf('0');  // no
        if (index != 0)  // is this a single leading zero?
          index = -1;  // no, use entire zoneString
        }
      else index = 1;  // yes, we have 2 leading zeroes
      if (index > -1) {
       postString = zoneString.substring(++index);
       preString = ' ';
       if (index == 2)
         preString = '  ';
       zoneString = preString + postString;
       }
      zoneNbr = parseInt(zoneString);
      if (DisplaySites.arguments.length == 1)  // do we have only one argument?
       totalString = zoneString + ' ' + ZoneName[zoneNbr] + ': ' + string;  // yes
      else {   // no, two arguments
       param2 = DisplaySites.arguments[1];   // fetch 2nd argument
       zoneString = param2.substring(3, 6);
       index = zoneString.indexOf('00');
       if (index != 0)  {  // is this 2 leading zeroes?
        index = zoneString.indexOf('0');  // no
        if (index != 0)  // is this a single leading zero?
          index = -1;  // no, use entire zoneString
        }
       else index = 1;  // yes, we have 2 leading zeroes
       if (index > -1) {
        postString = zoneString.substring(++index);
        preString = ' ';
        if (index == 2)
         preString = '  ';
        zoneString = preString + postString;
        totalString = zoneString + ' ' + ZoneName[zoneNbr] + ': ' + param2;
        }
       }
       console.log("totalString: "+totalString);
      // if (parent.deleteList)  {  // do we need to discard the list?
      //  ClearStrings();  // yes, clear it
      //  parent.setDeleteList(false);
      //  }
      // if (!parent.listMode)  {  // are we in list mode?
      //   i = 0  // no, always save entry in 1st location  
      //   parent.saveEntry(i++, totalString)
      //   parent.saveIndex(i)
      //   StatusBarLocked = 0
      //   StatusBar(-1, totalString, "Requested: ")
      //   StatusBarLocked = 5
      //   parent.WriteForm()  // after we write the form,  
      //   parent.SubmitForm()  // send it to server
      //   }
      // else  {  // yes, this is list mode
      // if (!parent.DoubleClick(totalString))  {  // was this entry already there?
      //   if (parent.SelectedIndex == MaxIndex)  {  // no, check for max entries
      //     alert("Maximum number of sites/areas have been selected!!")
      //     return
      //     }
      //   i = parent.SelectedIndex  
      //   parent.saveEntry(i++, totalString)
      //   parent.saveIndex(i)
      //   StatusBarLocked = 0
      //   StatusBar(-1, totalString, "Added: ")
      //   StatusBarLocked = 5
      //   parent.ToggleButton(0, "request1st.gif")
      //   parent.CookieRestored()
      //   parent.WriteForm()  
      //   }
      // }        
     }
      
   // If parameter zoneNumber = -1, display 2nd parameter (text string)
   // function StatusBar(zoneNumber)  {
   // // if (StatusBarLocked > 0)    {
   // //   --StatusBarLocked;
   // //   return true;
   // //   }
   // // parent.frames[2].document.open("text/html");
   // // parent.frames[2].document.write("<BODY BGCOLOR='#80FFFF'><BASEFONT SIZE='4'><CENTER>");
   // // if (StatusBar.arguments.length == 3) {
   // //   parent.frames[2].document.write(StatusBar.arguments[2]);
   // //   }
   // // if (zoneNumber > -1)
   // //   parent.frames[2].document.write(ZoneName[zoneNumber] + "</CENTER></BODY>");
   // // else
   // //   parent.frames[2].document.write(StatusBar.arguments[1] + "</CENTER></BODY>");
   // // parent.frames[2].document.close();
   // // return true;
   // }
   
   // function StatusLocked(entry)  {
   //   // StatusBarLocked = entry;
   //   }
   
   // function StatusClear()  {
   // // if (StatusBarLocked > 0)    {
   // //   --StatusBarLocked;
   // //   return true;
   // //   }   
   // // parent.frames[2].document.open("text/html");
   // // parent.frames[2].document.write("<BODY BGCOLOR='#80FFFF'></BODY>");
   // // parent.frames[2].document.close();
   // // return true;
   // }
   
   // Handle drop-down box for zone strings
   function DisplayStrings(flag)  {
   console.log("DisplayStrings : "+flag) 
   var zoneString, param1, param2, comma;
   if (flag == 1)
     zoneString = document.DropDown1.Zones.options[document.DropDown1.Zones.selectedIndex].value;
   else
     zoneString = document.DropDown2.Cities.options[document.DropDown2.Cities.selectedIndex].value;
   if (zoneString.indexOf("999") == -1)  {
    if (flag == 1)
      document.DropDown1.Zones.options.selectedIndex = 0;
     else
      document.DropDown2.Cities.options.selectedIndex = 0;
     comma = zoneString.indexOf(",");
     if (comma == -1)
      DisplaySites(zoneString);
     else   {
      param1 = zoneString.substring(0, comma);
      param2 = zoneString.substr(++comma, zoneString.length - comma);
      DisplaySites(param1, param2);
      }
     }
   }
   
   // Process drop-down boxes for generic strings of all types
 //   function DisplayTextValue(dropdownnumber)  {
 //   var valueString, textString;
 //   var i = 0;//parent.SelectedIndex;
 //   valueString = document.DropDown.elements[dropdownnumber].options[document.DropDown.elements[dropdownnumber].selectedIndex].value;
 //   console.log("DisplayTextValue: "+valueString);
 //   if (valueString.indexOf("999") == -1)  {     
 //      textString = document.DropDown.elements[dropdownnumber].options[document.DropDown.elements[dropdownnumber].selectedIndex].text + ' ' + valueString;
 //     document.DropDown.elements[dropdownnumber].options.selectedIndex = 0;
 //     console.log("DisplayTextValue: "+textString+" === "+valueString);
 //    // if (!parent.DeleteEntry(textString))  {  // was this entry already there?
 //    //     if (parent.SelectedIndex == MaxIndex)  {  // no, check if max entries
 //    //       alert("Maximum number of sites/areas have been selected!!");
 //    //       return;
 //    //       }
 //    //     // parent.saveEntry(i++, textString);  
 //    //     // parent.saveIndex(i);
 //    //     // StatusBarLocked = 0;
 //    //     // StatusBar(-1, textString, "Added: ");
 //    //     // StatusBarLocked = 5;
 //    //     }
 //    //  // parent.CookieRestored();
 //    //  // parent.WriteForm();
 //    //  }
 //   }
 // }
   
   // function ClearStrings()  {
   //  // parent.ClearStrings();
   //   }
   
   // function MainHelp()  {
   //    // parent.MainHelp();
   //    }

