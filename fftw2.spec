%define	oname	fftw
%define version	2.1.5
%define rel	12
%define release	%mkrel %{rel}

%define major	2
%define libname %mklibname %{oname} %{major}
%define develname %mklibname %{oname} -d %major

Name:		fftw2
Summary:	Fast fourier transform library
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/C
Source0:	%{oname}-%{version}.tar.bz2
Patch0:		%{oname}-2.1.3-pentium.patch
URL:		http://www.fftw.org/
%if %mdkversion <= 1020
BuildRequires:	gcc-g77
%else
BuildRequires:	gcc-gfortran
%endif
BuildRequires:	automake1.7
BuildRequires:	libtool

%description
FFTW is a collection of fast C routines for computing the Discrete Fourier
Transform in one or more dimensions.  It includes complex, real, and
parallel transforms, and can handle arbitrary array sizes efficiently.
This RPM package includes both the double- and single-precision FFTW
uniprocessor and threads libraries.  (The single-precision files have
an "s" prefix.)

%package -n	%{libname}
Summary:	Fast fourier transform library
Group:		Development/C

%description -n	%{libname}
FFTW is a collection of fast C routines for computing the Discrete Fourier
Transform in one or more dimensions.  It includes complex, real, and
parallel transforms, and can handle arbitrary array sizes efficiently.
This RPM package includes both the double- and single-precision FFTW
uniprocessor and threads libraries.  (The single-precision files have
an "s" prefix.)

%package -n	%{develname}
Summary:	Headers, libraries, & docs for FFTW fast fourier transform library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	fftw2-devel = %{version}-%{release}

%description -n %{develname}
This package contains the additional header files, documentation, and
libraries you need to develop programs using the FFTW fast fourier
transform library.

%prep
# We will be compiling two copies of FFTW, one for double precision and
# one for single precision.  During the build process, these copies
# will be stored in fftw-%{version}/double and fftw-%{version}/single

# Unpack the tar archive, first (-c) creating a fftw-%{version}
# directory and then unpacking in there.

%setup -q -c -n %oname-%version
# Now, rename the unpacked FFTW directory to "double":
mv %oname-%version double
# Apply patch to enable pentium optimizations
cd double
%patch0 -p1
cd ..
# Last, make a copy of this directory in "single":
cp -r double single

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
%ifarch %{ix86}
    %configure2_5x --enable-shared --enable-threads --infodir=$RPM_BUILD_ROOT%{_infodir} --enable-i386-hacks
%else
    %configure2_5x --enable-shared --enable-threads --infodir=$RPM_BUILD_ROOT%{_infodir}
%endif
%make

cd ../single
libtoolize --copy --force; aclocal-1.7; automake-1.7; autoconf
%ifarch %{ix86}
    %configure2_5x --enable-shared --enable-threads --infodir=$RPM_BUILD_ROOT%{_infodir} --enable-i386-hacks --enable-float --enable-type-prefix 
%else
    %configure2_5x --enable-shared --enable-threads --infodir=$RPM_BUILD_ROOT%{_infodir} --enable-float --enable-type-prefix
%endif
%make

%install
rm -rf $RPM_BUILD_ROOT
cd double
%makeinstall
cd ../single
%makeinstall

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

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{libname}
# run ldconfig to update the runtime linker database with the new libraries
# (make sure /sbin is in the $PATH)
PATH="/sbin:$PATH" ldconfig

%post -n %{develname}
%__install_info -e '* FFTW: (fftw).                     Fast Fourier Transform library.'\
                -s Libraries %{_infodir}/fftw.info.* %{_infodir}/dir

%preun -n %{develname}
%__install_info -e '* FFTW: (fftw).                     Fast Fourier Transform library.'\
                -s Libraries %{_infodir}/fftw.info.* %{_infodir}/dir --remove

%postun -n %{libname}
# after uninstall, run ldconfig to remove the libs from the linker database
PATH="/sbin:$PATH" ldconfig

%files -n %{libname}
%defattr (-,root,root)
%doc html FAQ doc/*ps doc/*fig doc/*tex* AUTHORS ChangeLog NEWS README* TODO
%{_libdir}/lib*fftw*.so.2*

%files -n %{develname}
%defattr (-,root,root)
%{_includedir}/*fftw*.h
%doc %{_infodir}/*
%{_libdir}/lib*fftw*.a
%{_libdir}/lib*fftw*.la
%{_libdir}/lib*fftw*.so
