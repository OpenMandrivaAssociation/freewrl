%global majorrel 4.3.0
%global commit e99ab4a000411dace7d3423ec37bdb7772998b1c
%global shortcommit %(c=%{commit}; echo ${c:0:8})
%global commitdate 20200221

%bcond_without java
%bcond_without docs

Name:		freewrl
Version:	%{majorrel}
Release:	16.%{commitdate}git%{shortcommit}%{?dist}
Summary:	X3D / VRML visualization program
License:	LGPLv3+
URL:		https://freewrl.sourceforge.net
# Source0:	http://sourceforge.net/projects/freewrl/files/freewrl-linux/3.0/%%{name}-%%{version}.tar.bz2
# git clone 	freewrl-git
# cd freewrl-git
# cp -a freex3d/ ../freewrl-%%{version}-%%{commitdate}git%%{shortcommit}
# cd ..
# tar --exclude-vcs -cjf %%{name}-%%{version}-%%{commitdate}git%%{shortcommit}.tar.bz2 freewrl-%%{version}-%%{commitdate}git%%{shortcommit}
Source0:	%{name}-%{version}-%{commitdate}git%{shortcommit}.tar.bz2
Source1:	README.FreeWRL.java
# gcc says:
# main/ProdCon.c:427:19: error: too few arguments to function 'cParse'
Patch3:		freewrl-3.0.0-20170208git621ae4e-cparse-stl-fix.patch
# warning: '__builtin_strncpy' output truncated before terminating nul copying 54 bytes from a string of the same length [-Wstringop-truncation]
Patch4:		freewrl-4.3.0-use-memcpy-instead-of-strncpy.patch
# main/ProdCon.c:414:29: warning: implicit declaration of function 'convertAsciiSTL' [-Wimplicit-function-declaration]
# main/ProdCon.c:424:29: warning: implicit declaration of function 'convertBinarySTL' [-Wimplicit-function-declaration]
Patch5:		freewrl-4.3.0-missing-functions.patch
# lots of indent issues caught by -Wmisleading-indentation
Patch6:		freewrl-4.3.0-fix-indent-issues.patch
# lots of signedness fixes like
# io_files.c:627:17: warning: pointer targets in passing argument 1 of 'stlDTFT' differ in signedness [-Wpointer-sign]
Patch7:		freewrl-4.3.0-sign-fixes.patch
Patch8: 	freewrl-c99.patch
Patch9:		freewrl-ffmpeg5.patch

BuildRequires:	doxygen
%if %{with java}
BuildRequires:	java-devel
%endif
BuildRequires:	imagemagick
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(imlib2)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(liblo)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(nspr)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xaw7)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(xv)
BuildRequires:	pkgconfig(zlib)
#BuildRequires:	ode-develBuildRequires:	sox
BuildRequires:	unzip
BuildRequires:	wget

Requires:	imagemagick
Requires:	sox
Requires:	unzip
Requires:	wget

%description
FreeWRL is an X3D / VRML visualization program. This package contains the
standalone commandline tool.

%files
%license COPYING COPYING.LESSER
%doc AUTHORS README TODO
%{_bindir}/%{name}
%{_bindir}/%{name}_msg
#{_bindir}/%{name}_snd
%{_libdir}/libFreeWRL.so.*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_mandir}/man1/%{name}*

#----------------------------------------------------------------------------

%package devel
Summary:	Development files for FreeWRL
Requires:	freewrl%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description devel
Development libraries and headers for FreeWRL.

%files devel
%{?with_docs:%doc doc/html}
%{_includedir}/libFreeWRL.h
%{_libdir}/libFreeWRL.so
%{_libdir}/pkgconfig/libFreeWRL.pc

#----------------------------------------------------------------------------

%if %{with java}
%package java
Summary:	Java support for FreeWRL
Requires:	java-headless
Requires:	freewrl%{?_isa} = %{version}-%{release}

%description java
Java support for FreeWRL.

%files java
%doc README.FreeWRL.java
%{_datadir}/%{name}/
/usr/lib/jvm/java-openjdk/jre/lib/ext/vrml.jar
%endif

#----------------------------------------------------------------------------

%package -n libEAI
Summary:	FreeWRL EAI C support library

%description -n libEAI
FreeWRL EAI C support library.


%files -n libEAI
%license COPYING COPYING.LESSER
%{_libdir}/libFreeWRLEAI.so.*

#----------------------------------------------------------------------------

%package -n libEAI-devel
Summary:	Development files for libEAI
Requires:	libEAI%{?_isa} = %{version}-%{release}

%description -n libEAI-devel
Development libraries and headers for libEAI.

%files -n libEAI-devel
%{_includedir}/FreeWRLEAI/
%{_libdir}/libFreeWRLEAI.so
%{_libdir}/pkgconfig/libFreeWRLEAI.pc

#----------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}-%{majorrel}-%{commitdate}git%{shortcommit}

# java
%if %{with java}
cp %{SOURCE1} .
%endif

# don't need it
rm -rf appleOSX/

# fix hardcoding /usr/local/lib is a no-no
sed -i 's|libpath = "/usr/local/lib"|libpath = "%{_libdir}"|g' src/bin/main.c

%build
%global optflags %{optflags} -Wno-comment -Wno-unused-variable -O2
#autoreconf --force --install
autoreconf -fiv
%configure \
	--disable-static \
	--disable-osc \
	--enable-fontconfig \
	%{?with_java:--enable-java} \
	--enable-libeai \
	--enable-libcurl \
	--enable-rbp \
	--enable-STL \
	--enable-twodee \
	--with-javadir=/usr/lib/jvm/java-openjdk/jre/lib/ext \
	--with-javascript=duk \
	--with-statusbar=hud \
	--with-target=x11 \
	%nil
%make_build

# html docs
pushd doc
%make html/index.html
popd

%install
%make_install # DESTDIR=%{buildroot}

# data dir
mkdir -p %{buildroot}%{_datadir}/%{name}/


#java
%if %{with java}
install -pm 0644 src/java/java.policy %{buildroot}%{_datadir}/%{name}/
%endif

# remove static stuff
rm -rf %{buildroot}%{_libdir}/*.a
rm -rf %{buildroot}%{_libdir}/*.la %{buildroot}%{_libdir}/mozilla/plugins/*.la

#chrpath --delete %{buildroot}%{_bindir}/freewrl
# chrpath --delete %%{buildroot}%%{_bindir}/freewrl_snd
#chrpath --delete %{buildroot}%{_libdir}/libFreeWRLEAI.so.*

