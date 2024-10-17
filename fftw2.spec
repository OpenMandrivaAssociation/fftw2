%define _empty_manifest_terminate_build 0

%define oname	fftw
%define major	2
%define libname 		%mklibname %{oname} %{major}
%define	libname_threads		%mklibname %{oname}_threads %{major}
%define	librname		%mklibname r%{oname} %{major}
%define	librname_threads	%mklibname r%{oname}_threads %{major}
%define	libsname		%mklibname s%{oname} %{major}
%define	libsname_threads	%mklibname s%{oname}_threads %{major}
%define	libsrname		%mklibname sr%{oname} %{major}
%define	libsrname_threads	%mklibname sr%{oname}_threads %{major}
%define devname 		%mklibname %{oname} -d %{major}

Summary:	Fast fourier transform library
Name:		fftw2
Version:	2.1.5
Release:	32
License:	GPLv2+
Group:		Development/C
Url:		https://www.fftw.org/
Source0:	http://www.fftw.org/%{oname}-%{version}.tar.gz
Patch0:		%{oname}-2.1.3-pentium.patch
Patch1:		fftw-linkage_fix.diff
Patch2:		fftw-2.1.5-automake-1.13.patch
Patch3:		fftw-2.1.5-texinfo51.patch

BuildRequires:	gcc-gfortran
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
Conflicts:	%{_lib}fftw2 < 2.1.5-19

%description -n	%{libname}
FFTW is a collection of fast C routines for computing the Discrete Fourier
Transform in one or more dimensions.  It includes complex, real, and parallel
transforms, and can handle arbitrary array sizes efficiently. This RPM package
includes both the double- and single-precision FFTW uniprocessor and threads
libraries.  (The single-precision files have an "s" prefix.)

%package -n	%{libname_threads}
Summary:	Fast fourier transform library
Group:		Development/C
Conflicts:	%{_lib}fftw2 < 2.1.5-19

%description -n	%{libname_threads}
This package contains a shared library for %{name}.

%package -n	%{librname}
Summary:	Fast fourier transform library
Group:		Development/C
Conflicts:	%{_lib}fftw2 < 2.1.5-19

%description -n	%{librname}
This package contains a shared library for %{name}.

%package -n	%{librname_threads}
Summary:	Fast fourier transform library
Group:		Development/C
Conflicts:	%{_lib}fftw2 < 2.1.5-19

%description -n	%{librname_threads}
This package contains a shared library for %{name}.

%package -n	%{libsname}
Summary:	Fast fourier transform library
Group:		Development/C
Conflicts:	%{_lib}fftw2 < 2.1.5-19

%description -n	%{libsname}
This package contains a shared library for %{name}.

%package -n	%{libsname_threads}
Summary:	Fast fourier transform library
Group:		Development/C
Conflicts:	%{_lib}fftw2 < 2.1.5-19

%description -n	%{libsname_threads}
This package contains a shared library for %{name}.

%package -n	%{libsrname}
Summary:	Fast fourier transform library
Group:		Development/C
Conflicts:	%{_lib}fftw2 < 2.1.5-19

%description -n	%{libsrname}
This package contains a shared library for %{name}.

%package -n	%{libsrname_threads}
Summary:	Fast fourier transform library
Group:		Development/C
Conflicts:	%{_lib}fftw2 < 2.1.5-19

%description -n	%{libsrname_threads}
This package contains a shared library for %{name}.

%package -n	%{devname}
Summary:	Headers, libraries, & docs for FFTW fast fourier transform library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libname_threads} = %{version}-%{release}
Requires:	%{librname} = %{version}-%{release}
Requires:	%{librname_threads} = %{version}-%{release}
Requires:	%{libsname} = %{version}-%{release}
Requires:	%{libsname_threads} = %{version}-%{release}
Requires:	%{libsrname} = %{version}-%{release}
Requires:	%{libsrname_threads} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
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
%patch3 -p1 

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

pushd double
libtoolize --copy --force; aclocal; automake --add-missing; autoconf
%configure2_5x \
	--disable-static \
	--enable-shared \
	--enable-threads \
%ifarch %{ix86}
	--enable-i386-hacks
%endif

%make

popd
pushd single
libtoolize --copy --force; aclocal; automake --add-missing; autoconf
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
popd

%install
%makeinstall_std -C double
%makeinstall_std -C single

# copy doc files where RPM will find them
# put the HTML stuff in a sperate dir, so it appears nicely in the docdir
pushd single
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
popd

%files -n %{libname}
%{_libdir}/libfftw.so.%{major}*

%files -n %{libname_threads}
%{_libdir}/libfftw_threads.so.%{major}*

%files -n %{librname}
%{_libdir}/librfftw.so.%{major}*

%files -n %{librname_threads}
%{_libdir}/librfftw_threads.so.%{major}*

%files -n %{libsname}
%{_libdir}/libsfftw.so.%{major}*

%files -n %{libsname_threads}
%{_libdir}/libsfftw_threads.so.%{major}*

%files -n %{libsrname}
%{_libdir}/libsrfftw.so.%{major}*

%files -n %{libsrname_threads}
%{_libdir}/libsrfftw_threads.so.%{major}*

%files -n %{devname}
%doc html FAQ doc/*ps doc/*fig doc/*tex* AUTHORS ChangeLog NEWS README* TODO
%{_includedir}/*fftw*.h
%{_libdir}/lib*fftw*.so
%{_infodir}/*

