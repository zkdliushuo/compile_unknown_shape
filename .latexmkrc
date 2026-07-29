use Cwd qw(getcwd);

# Keep BibTeX inputs rooted at the paper source directory even when latexmk
# writes auxiliary files to a separate output directory.
my $paper_source_dir = getcwd();
$ENV{'BIBINPUTS'} = $paper_source_dir . ':' . ($ENV{'BIBINPUTS'} // '');
$ENV{'BSTINPUTS'} = $paper_source_dir . ':' . ($ENV{'BSTINPUTS'} // '');

# BibTeX cannot write through an absolute auxiliary-file path under TeX Live's
# default openout policy. Run it inside the auxiliary directory instead.
$bibtex = 'cd %V && bibtex %O %B';
