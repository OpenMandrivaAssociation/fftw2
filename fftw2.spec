%define oname fftw

%define major 2
%define libname %mklibname %{oname} %{major}
%define develname %mklibname %{oname} -d %{major}

Summary:	Fast fourier transform library
Name:		fftw2
Version:	2.1.5
Release:	18
License:	GPLv2+
Group:		Development/C
URL:		http://www.fftw.org/
Source0:	%{oname}-%{version}.tar.bz2
Patch0:		%{oname}-2.1.3-pentium.patch
Patch1:		fftw-linkage_fix.diff
Patch2:		fftw-2.1.5-automake-1.13.patch
BuildRequires:	gcc-gfortran
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	texinfo

%description
FFTW is a collection of fast C routines for computing the Discrete Fourier
Transform in one or more dimensions.  It includes complex, real, and parallel
transforms, and can handle arbitrary array sizes efficiently. This RPM package
includes both the double- and single-precision FFTW uniprocessor and threads
libraries.  (The single-precision files have an "s" prefix.)

%package -n	%{libname}
Summary:	Fast fourier transform library
Group:		Development/C

%description -n	%{libname}
FFTW is a collection of fast C routines for computing the Discrete Fourier
Transform in one or more dimensions.  It includes complex, real, and parallel
transforms, and can handle arbitrary array sizes efficiently. This RPM package
includes both the double- and single-precision FFTW uniprocessor and threads
libraries.  (The single-precision files have an "s" prefix.)

%package -n	%{develname}
Summary:	Headers, libraries, & docs for FFTW fast fourier transform library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	fftw2-devel = %{version}-%{release}

%description -n %{develname}
This package contains the additional header files, documentation, andlibraries
you need to develop programs using the FFTW fast fourier transform library.

%prep
# We will be compiling two copies of FFTW, one for double precision and
# one for single precision.  During the build process, these copies
# will be stored in fftw-%{version}/double and fftw-%{version}/single

# Unpack the tar archive, first (-c) creating a fftw-%{version}
# directory and then unpacking in there.

%setup -q -c -n %{oname}-%{version}
# Now, rename the unpacked FFTW directory to "double":
mv %{oname}-%{version} double
# Apply patch to enable pentium optimizations
cd double
%patch0 -p1
cd ..
# Last, make a copy of this directory in "single":
cp -rp double single

%patch1 -p1

%patch2 -p1 -b .am113~

%build
# Configure and build the double and single precision versions.
# Notes:
#  (1) We install into ${RPM_BUILD_ROOT}, which is set either
#      by the BuildRoot option above or by --buildroot at build-time.
#      This allows you to build the RPM without blowing away your existing
#      FFTW installation, and even without being root.
#  (2) The double-precision version is installed with the normal library
#      names, while the single-precision version is installed with an "s"
#      prefix.

cd double
libtoolize --copy --force; aclocal; automake; autoconf
%configure2_5x \
    --disable-static \
    --enable-shared \
    --enable-threads \
%ifarch %{ix86}
    --enable-i386-hacks
%endif

%make

cd ../single
libtoolize --copy --force; aclocal; automake; autoconf
%configure2_5x \
    --disable-static \
    --enable-shared \
    --enable-threads \
%ifarch %{ix86}
    --enable-i386-hacks \
%endif
    --enable-float \
    --enable-type-prefix

%make

%install
cd double
%makeinstall_std

cd ../single
%makeinstall_std

# copy doc files where RPM will find them
# put the HTML stuff in a sperate dir, so it appears nicely in the docdir
mkdir -p ../html
cp doc/*html doc/*gif ../html
# remove HTML files from doc so that they don't appear double
rm -f doc/*html doc/*gif

# place the doc directory in a "findable" location
mkdir -p ../doc
cp -a doc/* ../doc

# the FAQ directory is also "nice" to have
mkdir -p ../FAQ
cp -a FAQ/* ../FAQ

# do the same to the other %doc files
cp AUTHORS ChangeLog NEWS README* TODO ..

%files -n %{libname}
%doc html FAQ doc/*ps doc/*fig doc/*tex* AUTHORS ChangeLog NEWS README* TODO
%{_libdir}/lib*fftw*.so.%{major}*

%files -n %{develname}
%{_includedir}/*fftw*.h
%{_libdir}/lib*fftw*.so
%{_infodir}/*

%changelog
* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 2.1.5-15mdv2011.0
+ Revision: 627774
- don't force the usage of automake1.7

* Wed Aug 05 2009 Götz Waschk <waschk@mandriva.org> 2.1.5-14mdv2011.0
+ Revision: 409959
- update license

* Mon Aug 04 2008 Oden Eriksson <oeriksson@mandriva.com> 2.1.5-13mdv2009.0
+ Revision: 262954
- fix linkage (P1)

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 2.1.5-12mdv2008.1
+ Revision: 136415
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Aug 31 2007 Götz Waschk <waschk@mandriva.org> 2.1.5-12mdv2008.0
+ Revision: 77011
- revert previous devel name change

* Fri Aug 31 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1.5-11mdv2008.0
+ Revision: 76951
- new devel naming
- fix info-install
- bunzip the patch

* Thu Aug 30 2007 Götz Waschk <waschk@mandriva.org> 2.1.5-10mdv2008.0
+ Revision: 76343
- clean obsoletes and provides

* Tue Jul 24 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1.5-9mdv2008.0
+ Revision: 54961
- make it build
- Import fftw2



* Thu Jul 20 2006 Götz Waschk <waschk@mandriva.org> 2.1.5-9mdk
- Rebuild

* Wed Feb 08 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 2.1.5-8mdk
- rebuild

* Wed Jul 06 2005 Per Ãyvind Karlsen <pkarlsen@mandriva.com> 2.1.5-7mdk
- fix so we're using g77 as compiler for older releases
- %%mkrel
- wipe out buildroot in %%install, not %%prep
- cosmetics

* Wed May 25 2005 Götz Waschk <waschk@mandriva.org> 2.1.5-6mdk
- rebuild with gfortran

* Sun Dec 26 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.1.5-5mdk
- lib64 fix

* Fri Dec  3 2004 GÃ¶tz Waschk <waschk@linux-mandrake.com> 2.1.5-4mdk
- rebuild

* Thu Nov 20 2003 GÃ¶tz Waschk <waschk@linux-mandrake.com> 2.1.5-3mdk
- fix build and dependancies
- fix devel provides
- reintroduce libfftw2 for compatiblity 

* Thu Jul 10 2003 GÃ¶tz Waschk <waschk@linux-mandrake.com> 2.1.5-2mdk
- mklibname macro
- autoconf 2.5 macro
- quiet tar

* Tue Mar 25 2003 Lenny Cartier <lenny@mandrakesoft.com> 2.1.5-1mdk
- 2.1.5

* Sat Jan 18 2003 Lenny Cartier <lenny@mandrakesoft.com> 2.1.3-11mdk
- rebuild

* Tue Sep 03 2002 Lenny Cartier <lenny@mandrakesoft.com> 2.1.3-10mdk
- fix provides/obsoletes

* Wed Aug 28 2002 Lenny Cartier <lenny@mandrakesoft.com> 2.1.3-9mdk
- rebuild

* Thu Jun 14 2001 Lenny Cartier <lenny@mandrakesoft.com> 2.1.3-8mdk
- fixed by Mika Korhonen <mikak@ee.oulu.fi> :
	- removed broken ld.so.conf test (/usr/lib is not listed there anyways)
	- made install-info work with RPM macros shipping with newer Mandrakes
	  and actually add an entry to the top dir file

* Tue Jan 09 2001 Lenny Cartier <lenny@mandrakesoft.com> 2.1.3-7mdk
- rebuild

* Tue Aug 31 2000 Lenny Cartier <lenny@mandrakesoft.com> 2.1.3-6mdk
- add installinfo

* Wed Aug 30 2000 Alexander Skwar <ASkwar@DigitalProjects.com> 2.1.3-5mdk
- Actually used macros
- Added %%doc files
- Shortened %%files section of the SPEC file a lot
- Provide libfftw as eXtace requires it
- Obsolote libfftw package
- Optimized for Pentium builds per README.hacks

* Wed Aug 30 2000 Lenny Cartier <lenny@mandrakesoft.com> 2.1.3-4mdk
- BM
- macros

* Wed Apr 26 2000 Lenny Cartier <lenny@mandrakesoft.com> 2.1.3-3mdk
- fix group
- spec helper fixes

* Tue Jan 25 2000 Lenny Cartier <lenny@mandrakesoft.com>
- updated, installs in /usr instead of /usr/local by Dara Hazeghi
  <dara@pacbell.net>

* Thu Dec 16 1999 Lenny Cartier <lenny@mandrakesoft.com>
- new in contribs
- bz2 archive 
- add defattr
