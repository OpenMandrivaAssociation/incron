%define name incron
%define version 0.5.8
%define release %mkrel 1

Summary: An inotify based cron daemon
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.bz2
Source1: incron.initscript
Patch0:  incron-Makefile-missing-man.patch
License: GPL
Group: System/Servers
Url: http://incron.aiken.cz/
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: gcc-c++

%description
incron is an "inotify cron" system. It works like the regular cron but is
driven by filesystem events instead of time periods. It contains two
programs, a daemon called "incrond" (analogous to crond) and a table
manipulator "incrontab" (like "crontab").

%prep
%setup -q
%patch0 -p0 -b .missing-man

%build
%make OPTIMIZE="%optflags" PREFIX=%_prefix

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p %buildroot{%_sbindir,%_bindir}

make install \
    PREFIX=%buildroot%_prefix \
    USERDATADIR=%buildroot/var/spool/incron \
    SYSDATADIR=%buildroot%_sysconfdir/incron.d \
    CFGDIR=%buildroot%_sysconfdir \
    MANPATH=%buildroot%_mandir \
    USER=$USER

install -m644 incron.conf.example %buildroot%_sysconfdir/incron.conf

mkdir -p %buildroot%_sysconfdir/init.d/
install -m 755 %SOURCE1 %buildroot%_sysconfdir/init.d/incrond

%post
%_post_service incrond

%preun
%_preun_service incrond

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc CHANGELOG README TODO
%doc doc/html
%attr(4755,root,root) %_bindir/incrontab
%_sbindir/incrond
/var/spool/incron
%_sysconfdir/incron.d
%_sysconfdir/incron.conf.example
%config(noreplace) %_sysconfdir/incron.conf
%_mandir/man?/*
%_sysconfdir/init.d/incrond


