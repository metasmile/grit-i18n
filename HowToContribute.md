# Contributing to GRIT #

Please feel free to contribute patches to GRIT.  If you have a new project using GRIT, please let us know by sending a message to the developer group (http://groups.google.com/group/grit-developer), and join the user group (http://groups.google.com/group/grit-users).  Also, note the RegressionTestPlan that describes how we ensure GRIT stays compatible with your project.

Those who send the occasional patch should ask one of the project committers (https://code.google.com/p/grit-i18n/people/list) to land their patch for them after review.  Please read the following section on preparing patches for review.

Those who have submitted several patches and expect to submit patches on a regular basis should request to become committers.  See the section below on that.

## Preparing Patches ##

You should read the GritUsersGuide and the DesignOverview for background on the intended usage and design of GRIT.  For more details or for help with how to design your patch, ask one of the project committers.

We use the Chromium depot\_tools to upload patches to the Rietveld review tool.  Please install the tools (http://www.chromium.org/developers/how-tos/install-depot-tools) and then use `gcl upload` (if you use SVN) or `git cl upload` (if you use git) to upload a patch before you send it for review.

Before sending patches for review, make sure `grit.py unit` runs without warnings.

For large patches, it is advisable to discuss with committers on the project first, either by mailing a specific committer you think knows the code you are changing, or by mailing the developer list.  It is also advisable to test large patches with Chromium before sending it for review, as it is the largest known open-source project using GRIT, so it exercises many features.  To do this:
  * Follow the Chromium instructions for setting up a checkout (see http://www.chromium.org/developers/how-tos), and make sure you are able to fetch and build the Chromium code.
  * Add the custom\_deps section below this list to your .gclient file. This causes your checkout not to fetch the standard version of GRIT.
  * Delete src/tools/grit (e.g. `rm -rf src/tools/grit`).
  * Instead, check out this project to src/tools/grit (e.g. `cd src/tools && svn checkout http://grit-i18n.googlecode.com/svn/trunk/ grit`).
  * You now have a version of Chromium that uses whatever changes you have in your src/tools/grit directory, so you can build Chromium, check that the build succeeds, check that `gclient runhooks` succeeds, etc.

```
    "custom_deps" : {
      "src/tools/grit": None,
    }
```

## Becoming a Committer ##

There are two ways to become a committer:
  * If you are a committer on an open-source project that uses GRIT:  First, submit ~5 high-quality patches to the project, then solicit the support of one of the project owners, and at least one other committer.
  * For those who are not committers on open-source projects using GRIT, the bar is ~10 high-quality patches, and support from one project owner plus two committers.

Committers must act in the best interest of the project.  Project owners reserve the right to revoke committer status.  Committer status may also be revoked when a committer has not been active for 9-12 months.