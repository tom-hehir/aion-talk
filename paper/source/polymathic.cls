% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Polymathic class — minimally diverged from FAIR pre-print style
% Requests applied:
%  - Title moved under first rule; logo stays above
%  - Date moved down (out of top-right meta block)
%  - "Abstract" label bigger
%  - Affiliations smaller
%  - Tighter spacing between authors↔affiliations and affiliations↔contribs
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{polymathic}
\LoadClassWithOptions{article}

% Layout %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage[top=2.25cm, bottom=2.5cm, left=2.5cm, right=2.5cm, columnsep=0.65cm]{geometry}
\RequirePackage{microtype}
\RequirePackage{placeins}
\RequirePackage{hyphenat}
\RequirePackage{setspace}
\RequirePackage{parskip}
\RequirePackage[latin, english]{babel}
\RequirePackage{lipsum}
\RequirePackage{etoolbox}

\DisableLigatures[f]{family=sf*} 

% Graphics %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage{graphicx}
\RequirePackage{subcaption}

% Tables %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage{booktabs}
\RequirePackage{nicematrix}
\RequirePackage{multirow}
\RequirePackage{bm}
\newcommand{\nm}[1]{#1}

% Colors (kept for links/accents) %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage[most]{tcolorbox} % available to users; not used in title
\RequirePackage{xcolor}
\definecolor{polyred}{HTML}{CA0E4C}
\definecolor{metafg}{HTML}{1C2B33}
\definecolor{metabg}{HTML}{F1F4F7}

% References %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage{hyperref}
\RequirePackage[noabbrev,nameinlink]{cleveref}
\hypersetup{
  colorlinks,
  linkcolor=polyred,
  citecolor=polyred,
  urlcolor=polyred
}

\RequirePackage[sort&compress]{natbib}
\def\bibfont{\small}

% Section and caption format %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage{titlesec}
\titleformat*{\paragraph}{\itshape\sffamily}
\titleformat*{\section}{\Large\sffamily\bfseries}
\titleformat*{\subsection}{\large\sffamily\bfseries}
\titleformat*{\subsubsection}{\normalsize\sffamily\bfseries}
\DeclareTextFontCommand{\textbf}{\bfseries\sffamily}

\RequirePackage{caption}
% Diverge from FAIR's custom caption format: standard hanging style with colon
\captionsetup{
  singlelinecheck=false,
  format=plain,        % was: hang
  labelsep=colon,
  labelfont={bf,sf},
  font=small,
  justification=justified % optional: or raggedright
}
\captionsetup[sub]{
  singlelinecheck=true,
  format=plain,        % was: hang
  labelsep=colon,
  labelfont={bf,sf},
  font=small,
  justification=justified
}

% Fonts %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\renewcommand*\ttdefault{cmvtt}
\RequirePackage[LY1]{fontenc}

\DeclareFontFamily{LY1}{optimistic}{}
\DeclareFontShape{LY1}{optimistic}{m}{n}{<-> s * [0.88] assets/optimistic}{}
\pdfmapline{+optimistic < assets/Optimistic.ttf <texnansi.enc}
\renewcommand{\sfdefault}{optimistic}

% Authors, affiliations, metadata %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\makeatletter
\renewcommand\addtolist[5][]{
  \begingroup
    \if\relax#3\relax\def\sep{}\else\def\sep{#5}\fi
    \let\protect\@unexpandable@protect 
    \xdef#3{\expandafter{#3}\sep #4[#1]{#2}}%
  \endgroup
}
\makeatother

\newcommand\authorlist{}
\newcommand\authorformat[2][]{{\sffamily \bfseries #2$^{#1}$}}
\renewcommand\author[2][]{\addtolist[#1]{#2}{\authorlist}{\authorformat}{, }}

\newcommand\affiliationlist{}
% Smaller affiliations (changed from \normalsize)
\newcommand\affiliationformat[2][]{{\small $^{#1}$#2}}
\newcommand\affiliation[2][]{\addtolist[#1]{#2}{\affiliationlist}{\affiliationformat}{, }}

\newcommand\contributionlist{}
\newcommand\contributionformat[2][]{{\small $^{#1}$#2}}
\newcommand\contribution[2][]{\addtolist[#1]{#2}{\contributionlist}{\contributionformat}{, }}

\newcommand\metadatalist{} % top-right meta (e.g., Correspondence)
\newcommand\metadataformat[2][]{{\small {\sffamily \bfseries #1:} #2}}
\newcommand\metadata[2][]{\addtolist[#1]{#2}{\metadatalist}{\metadataformat}{\par}}

% Date stored separately so we can move it "down"
\newcommand\datelist{}
\renewcommand\date[1]{\gdef\datelist{{{\sffamily \bfseries Date:} #1}}}

\newcommand\titlecorrespondencelist{}
\newcommand\titlecodelist{}

% Setters (use in the paper preamble)
\newcommand{\titlecorrespondence}[1]{%
  \gdef\titlecorrespondencelist{{{\sffamily \bfseries Correspondence:} #1}}}

\newcommand{\titlecode}[1]{%
  \gdef\titlecodelist{{{\sffamily \bfseries Code:} #1}}}



\newcommand{\corrlst}{}

% Abstract + helpers
\newcommand{\abstractlist}{}
\renewcommand{\abstract}[1]{\def\abstractlist{{\color{metafg} #1}}}
\newcommand{\email}[1]{\href{mailto:#1}{\texttt{#1}}}

\newcommand\correspondence[1]{\metadata[Correspondence]{#1}}

\renewcommand{\title}[1]{\newcommand{\titlelist}{{\huge\sffamily\bfseries #1}}}

\newcommand{\beginappendix}{\appendix{\huge\sffamily Appendix\par}}

% Title block (no shaded box) %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Layout now:
%   [Logo + top-right meta (no Date)]
%   --- rule ---
%   Title
%   Authors
%   Affiliations (smaller)
%   Contributions (tight)
%   Date (moved down)
%   "Abstract" (bigger) + text
%   --- rule ---

\newcommand{\polytopbar}{%
  \noindent
  {\color{polyred}\rule{\linewidth}{1.6pt}}%
  \llap{\makebox[\linewidth]{\hfil{\color{black}\rule{0.70\linewidth}{1.6pt}}\hfil}}%
}

% Bottom: full-width black rule
\newcommand{\polybottombar}{%
  \noindent{\color{black}\rule{\linewidth}{1.6pt}}\par
}

% A light, rounded box for the title/abstract block
% (tcolorbox already loaded with [most])
\newtcolorbox{polytitlebox}[1][]{%
  enhanced,
  frame hidden,
  boxrule=0pt,
  colback=metabg,
  arc=10pt,
  left=0.5cm,
  right=0.5cm,
  top=0.5cm,
  bottom=0.5cm,
  before skip=0.6em,
  after  skip=0.6em,
  #1
}

\newcommand{\mymaketitle}{%
  \setlength{\parindent}{0pt}
  \setlength{\parskip}{0.4cm}

  % Top-right: logo and (non-date) metadata
  \begingroup
    \setlength{\parskip}{0pt}
    \noindent
    \raggedleft
    \includegraphics[width=3.5cm]{assets/polymathic_logo_black.png}\par
    \ifdefempty{\metadatalist}{}{%
      \vspace{0.4em}
      {\small\setlength{\parskip}{0.25em}\metadatalist}%
    }
  \endgroup

  % Faded box wrapping: Title + authors/affils/contribs + date + abstract
  \begin{polytitlebox}
    % Title under the rule
    {\raggedright
      {\setstretch{1.35}\titlelist\par}
    }

    % Authors / affiliations / contributions with tighter spacing
    \begingroup
      \setlength{\parskip}{0pt} % tighten locally
      \vspace{0.6em}
      {\raggedright \authorlist\par}
      % ↓ smaller gap between authors and affiliations
      \vspace{0.1cm}
      {\raggedright \affiliationlist\par}
      % ↓ smaller gap between affiliations and contributions
      \vspace{0.05cm}
      {\raggedright \contributionlist\par}
    \endgroup

    % Abstract content (no explicit "Abstract" label, as in your current .cls)
    \ifdefempty{\abstractlist}{}{%
      \vspace{0.5em}
      \abstractlist\par
    }

    % Date (kept down here, out of meta block)
    \ifdefempty{\datelist}{}{{
    \vspace{0.5em}
    \raggedright 
    {\small \datelist}\par}}

    % Optional: Correspondence (under Date)
    \ifdefempty{\titlecorrespondencelist}{}{{
      \vspace{0.25em}
      \raggedright
      {\small \titlecorrespondencelist}\par
    }}
    
    % Optional: Code (under Date)
    \ifdefempty{\titlecodelist}{}{{
      \vspace{0.1em}
      \raggedright
      {\small \titlecodelist}\par
    }}


    
  \end{polytitlebox}

  \FloatBarrier
}

% Maketitle wrappers for one-/two-column %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\makeatletter
\if@twocolumn%
  \renewcommand{\maketitle}{%
    \twocolumn[%
      \mymaketitle
      \vskip 0.35cm
    ]%
  }%
\else%
  \renewcommand{\maketitle}{%
    \mymaketitle
  }%
\fi
\makeatother