Summary:	Filter-style and IJS printer drivers, printer maintenance utilities
Name:		printer-tools
Version:	2008
Release:	20
License:	GPLv2
Group:		Publishing
Url:		http://www.linuxprinting.org/

# Perl script to clean up Manufacturer entries in the PPD files, so that
# drivers are sorted by the printer Manufacturer in the graphical frontends
Source201: 	cleanppd.pl

# Script to adjust margins and offsets of printed pages
Source75: 	alignmargins
Source175:	align.ps

# Tool for uploading the firmware on the HP LaserJet 1000S
Source85:	http://www.linuxprinting.org/download/printing/hp1000fw

# Tools for reading USB device ID strings
Source87:	http://www.linuxprinting.org/download/printing/usb_id_test.c
Source88:	http://www.linuxprinting.org/download/printing/getusbprinterid.pl

%description
Tools for printer maintenance: Setting default options for most laser
printers (PJL-capable printers), cartridge changing, head aligning,
ink level checking for inkjet printers. Printing big posters on many 
sheets of standard sized paper (A4, A3, Letter, ...) to be assambled
together (also used by KDE Print to print posters).

%prep
%setup -q -c -T

# Tool for uploading the firmware on the HP LaserJet 1000S
cp %{SOURCE85} hp1000fw

# Tools for reading USB device ID strings
cp %{SOURCE87} usb_id_test.c
cp %{SOURCE88} getusbprinterid

%build
# Tool for reading USB device ID strings
gcc %{optflags} %{ldflags} -o usb_id_test usb_id_test.c

%install
# Make directories
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_includedir}
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_mandir}/man8
install -d %{buildroot}%{_libdir}/gimp/2.0/plug-ins
install -d %{buildroot}%{_prefix}/lib/cups/filter
install -d %{buildroot}%{_prefix}/lib/cups/backend
install -d %{buildroot}%{_datadir}/cups/data
install -d %{buildroot}%{_datadir}/cups/model
install -d %{buildroot}%{_sysconfdir}/cups
install -d %{buildroot}%{_datadir}/foomatic/db/source/printer
install -d %{buildroot}%{_datadir}/foomatic/db/source/driver
install -d %{buildroot}%{_datadir}/foomatic/db/source/opt

# Install margin and offset adjustment script in /usr/sbin
cp %{SOURCE75} %{buildroot}%{_sbindir}/alignmargins

# Adjust path to improved align.ps 
perl -p -i -e 's:/usr/share/ghostscript/\*/lib/align.ps:%{_datadir}/alignmargins/align.ps:' %{buildroot}%{_sbindir}/alignmargins

# Install improved align.ps
install -d %{buildroot}%{_datadir}/alignmargins/
cp %{SOURCE175} %{buildroot}%{_datadir}/alignmargins/align.ps

# Install a script to display the test page on the screen for colour
# adjustment
cat <<EOF > %{buildroot}%{_bindir}/displaytestpage
#!/bin/sh
ps2img="gs -dQUIET -dNOPAUSE -dBATCH -sDEVICE=pnm -r75x75 -sOUTPUTFILE=- -"
testpage=/usr/share/cups/data/testprint.ps

TMPFILE=~/.displaytestpage.pnm
if [ -x /usr/bin/kview ]; then
  cat \$testpage | \$ps2img > \$TMPFILE 
  /usr/bin/kview \$TMPFILE
elif [ -x /usr/bin/ee ]; then
  cat \$testpage | \$ps2img > \$TMPFILE 
  /usr/bin/ee \$TMPFILE
elif [ -x /usr/bin/gqview ]; then
  cat \$testpage | \$ps2img > \$TMPFILE 
  /usr/bin/gqview \$TMPFILE
elif [ -x /usr/bin/xv ]; then
  cat \$testpage | \$ps2img | /usr/bin/xv -
elif [ -x /usr/bin/kghostview ]; then
  /usr/bin/kghostview \$testpage
elif [ -x /usr/X11R6/bin/gv ]; then
  /usr/X11R6/bin/gv \$testpage
elif [ -x /usr/X11R6/bin/ghostview ]; then
  /usr/X11R6/bin/ghostview \$testpage
else
  xmessage "No suitable program for viewing PostScript found, install GhostView, gv, or similar."
  exit 1
fi
rm \$TMPFILE
EOF
chmod a+rx %{buildroot}/usr/bin/displaytestpage

# Tool for uploading the firmware on the HP LaserJet 1000S
install -m 0755 hp1000fw %{buildroot}%{_bindir}

install -d %{buildroot}%{_sysconfdir}/printer

# Tools for reading USB device ID strings
install -m0755 usb_id_test %{buildroot}%{_bindir}
install -m0755 getusbprinterid %{buildroot}%{_bindir}

# "cleanppd.pl" removes unwished PPD files fixes broken manufacturer
# entries, and cleans lines which contain only spaces and tabs.

# Uncompress Perl script for cleaning up the PPD files
#cp %{SOURCE201} ./cleanppd.pl
#chmod a+rx ./cleanppd.pl

# Do the clean-up
#find %{buildroot}%{_datadir}/cups/model -name "*.ppd" -exec ./cleanppd.pl '{}' \;

# Remove PPDs which are not Adobe-compliant and therefore not working with
# CUPS 1.1.20
#for ppd in `find %{buildroot}%{_datadir}/cups/model -name "*.ppd.gz" -print`; do cupstestppd -q $ppd || (rm -f $ppd && echo "$ppd not Adobe-compliant. Deleted."); done

%files
%attr(0755,root,root) %{_sbindir}/alignmargins
%attr(0755,root,root) %{_bindir}/hp1000fw
%attr(0755,root,root) %{_bindir}/displaytestpage
%attr(0755,root,root) %{_bindir}/usb_id_test
%attr(0755,root,root) %{_bindir}/getusbprinterid
%{_datadir}/alignmargins

