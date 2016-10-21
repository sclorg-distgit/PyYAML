%{?scl:%scl_package PyYAML}
%{!?scl:%global pkg_name %{name}}

Name:           %{?scl_prefix}PyYAML
Version:        3.10
Release:        14%{?dist}
Summary:        YAML parser and emitter for Python

Group:          Development/Libraries
License:        MIT
URL:            http://pyyaml.org/
Source0:        http://pyyaml.org/download/pyyaml/%{pkg_name}-%{version}.tar.gz
BuildRequires:  %{?scl_prefix}python-devel, 
BuildRequires:  %{?scl_prefix}python-setuptools
BuildRequires:  libyaml-devel
Provides:       %{?scl_prefix}python-yaml = %{version}-%{release}
Provides:       %{?scl_prefix}python-yaml%{?_isa} = %{version}-%{release}

# http://pyyaml.org/ticket/247
Patch0: PyYAML-size_t_not_int.patch

%{?scl:Requires: %{scl}-runtime}
%{?scl:BuildRequires: %{scl}-runtime}

%description
YAML is a data serialization format designed for human readability and
interaction with scripting languages.  PyYAML is a YAML parser and
emitter for Python.

PyYAML features a complete YAML 1.1 parser, Unicode support, pickle
support, capable extension API, and sensible error messages.  PyYAML
supports standard YAML tags and provides Python-specific tags that
allow to represent an arbitrary Python object.

PyYAML is applicable for a broad range of tasks from complex
configuration files to object serialization and persistance.

%prep
%setup -q -n %{pkg_name}-%{version}
chmod a-x examples/yaml-highlight/yaml_hl.py

# Remove shebang from yaml_hl.py
sed -i 's|#!/usr/bin/python||' examples/yaml-highlight/yaml_hl.py

%patch0 -p1

%build
%{?scl:scl enable %{scl} - << \EOF}
CFLAGS="${RPM_OPT_FLAGS}" %{__python} setup.py --with-libyaml build
%{?scl:EOF}

%install
rm -rf %{buildroot}
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py install -O1 --skip-build --root %{buildroot} \
    --install-purelib %{python_sitelib} \
    --install-platlib %{python_sitearch}
%{?scl:EOF}

%check
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py test
%{?scl:EOF}

%files
%defattr(644,root,root,755)
%doc CHANGES LICENSE PKG-INFO README examples
%{python_sitearch}/*

%changelog
* Mon Apr 25 2016 Charalampos Stratakis <cstratak@redhat.com> - 3.10-14
- Remove shebang from yaml_hl.py example file
Resolves: rhbz#1330146

* Fri Feb 12 2016 Robert Kuska <rkuska@redhat.com> - 3.10-13
- Rebuilt for python27 rhscl

* Thu May 22 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 3.10-12
- Rebuilt for devassist09
- Don't regenerate cython .pyx files to avoid Cython dependency

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 3.10-11
- Mass rebuild 2014-01-24

* Tue Jan  7 2014 John Eckersberg <jeckersb@redhat.com> - 3.10-10
- Add patch to fix build issue on s390x (bz1048898)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.10-9
- Mass rebuild 2013-12-27

* Thu Aug  8 2013 John Eckersberg <jeckersb@redhat.com> - 3.10-8
- Add check section and run test suite

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 3.10-6
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Wed Aug  1 2012 David Malcolm <dmalcolm@redhat.com> - 3.10-5
- remove rhel logic from with_python3 conditional

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 27 2012 John Eckersberg <jeckersb@redhat.com> - 3.10-3
- Add Provides for python-yaml (BZ#740390)

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 23 2011 John Eckersberg <jeckersb@redhat.com> - 3.10-1
- New upstream release 3.10

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.09-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 John Eckersberg <jeckersb@redhat.com> - 3.09-7
- Add support to build for python 3

* Tue Jul 27 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 3.09-6
- Bump release number for upgrade path

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.09-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Oct 02 2009 John Eckersberg <jeckersb@redhat.com> - 3.09-1
- New upstream release 3.09

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.08-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 - John Eckersberg <jeckersb@redhat.com> - 3.08-5
- Minor tweaks to spec file aligning with latest Fedora packaging guidelines
- Enforce inclusion of libyaml in build with --with-libyaml option to setup.py
- Deliver to %%{python_sitearch} instead of %%{python_sitelib} due to _yaml.so
- Thanks to Gareth Armstrong <gareth.armstrong@hp.com>

* Tue Mar 3 2009 John Eckersberg <jeckersb@redhat.com> - 3.08-4
- Correction, change libyaml to libyaml-devel in BuildRequires

* Mon Mar 2 2009 John Eckersberg <jeckersb@redhat.com> - 3.08-3
- Add libyaml to BuildRequires

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 John Eckersberg <jeckersb@redhat.com> - 3.08-1
- New upstream release

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 3.06-2
- Rebuild for Python 2.6

* Fri Oct 24 2008 John Eckersberg <jeckersb@redhat.com> - 3.06-1
- New upstream release

* Wed Jan 02 2008 John Eckersberg <jeckersb@redhat.com> - 3.05-2
- Remove explicit dependency on python >= 2.3
- Remove executable on example script in docs

* Mon Dec 17 2007 John Eckersberg <jeckersb@redhat.com> - 3.05-1
- Initial packaging for Fedora
