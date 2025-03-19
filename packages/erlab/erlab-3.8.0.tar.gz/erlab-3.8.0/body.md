## v3.8.0 (2025-03-11)

### ✨ Features

- **kspace:** add method to convert between experimental configurations ([7a426a8](https://github.com/kmnhan/erlabpy/commit/7a426a85c0346c7fcf9e9f5e78f2cafc2b9701b7))

  Adds a new method `DataArray.kspace.as_configuration` that allows the user to easily correct data loaded in the wrong configurations. This is useful for setups where the experimental geometry can be changed.

- **io.plugins:** add `mbs` plugin for setups based on MB Scientific AB analyzers (#112) ([43e454b](https://github.com/kmnhan/erlabpy/commit/43e454b1b27aa9a538449875b2df92284a845c8f))

- **imagetool:** add Symmetrize dialog ([4ebaeab](https://github.com/kmnhan/erlabpy/commit/4ebaeabf7d0c34420e4b32080a2ac96641aca228))

- **imagetool.dialogs:** enhance CropToViewDialog with dimension selection and validation ([6394121](https://github.com/kmnhan/erlabpy/commit/6394121c9f428d522dd919e98451598b417fa1fb))

- **imagetool:** add Average dialog for averaging data over selected dimensions ([2e81aec](https://github.com/kmnhan/erlabpy/commit/2e81aecb88fe057d2028191bb9ff5da5044c6175))

- **imagetool:** include rotation angle in rotation transform suffix ([2842c5f](https://github.com/kmnhan/erlabpy/commit/2842c5f0a29b4a49e7b2ef9945f7380e04f2b3e4))

- **imagetool.manager:** add new action to refresh ImageTool data from the file it was loaded from. ([d822f73](https://github.com/kmnhan/erlabpy/commit/d822f7378291781a3ced5a4834f7c99220a3bf9f))

  When performing real-time data analysis, it is often necessary to update the data in the ImageTool from the file it was loaded from. This commit adds a new `Reload Data` action to the right-click context menu of the ImageTool manger. The action is only visible when the data can be properly reloaded.

- **imagetool:** retain cursor info when loading new data that is compatible with the current data ([917851f](https://github.com/kmnhan/erlabpy/commit/917851fd9be8375f374eb6e2ea0db7d68d40d124))

- **analysis.gold:** `gold.poly` now returns a fit result Dataset instead of a  lmfit modelresult. ([ff224e7](https://github.com/kmnhan/erlabpy/commit/ff224e7d16ef7c104a1f54ab93b16d02b989cbaf))

- **analysis.gold:** add background slope option for Fermi edge fitting ([513e531](https://github.com/kmnhan/erlabpy/commit/513e531f7fb44365841b8079e36fcabe8f86254a))

- **io:** allow temporary overriding of loader properties (#101) ([bd4c50b](https://github.com/kmnhan/erlabpy/commit/bd4c50bb7cde93ea9a0d88dfb442349f18985fe0))

  Adds a new context manager, `erlab.io.extend_loader`, for temporarily overriding data loader behaviour.

  This is especially useful for data across multiple files, where the user can specify additional attributes to treat as coordinates, allowing them to be concatenated.

- **explorer:** add image preview and fine-grained loading control ([dca8fcb](https://github.com/kmnhan/erlabpy/commit/dca8fcb6f4803cce39436d7610c98c9ebe2e9403))

- **imagetool:** implement non-dimension coordinate plotting ([48eac24](https://github.com/kmnhan/erlabpy/commit/48eac242e0d08fba8aa5e4f5e94c05d6db144003))

  1D Non-dimension coordinates associated with a data dimension can now be plotted alongside 1D slices on a secondary axis.

  For instance, if an ARPES map has a temperature coordinate that varies for each mapping angle, the temperature coordinate can be plotted as a function of angle.

  The plot can be toggled in the added item inside the `View` menu of the menu bar in ImageTool.

- add accessor method for averaging over dimensions while retaining coordinates ([90d28fb](https://github.com/kmnhan/erlabpy/commit/90d28fbe27114e6191b2b777c3d8fefc96e607cb))

  Adds `DataArray.qsel.average`, which takes dimension names and calls `DataArray.qsel` with the bin widths set to infinity. Unlike `DataArray.mean`, the new method retains coordinates associated with the averaged dimension.

- **analysis.fit.functions:** make several fitting functions xarray-aware ([53b3688](https://github.com/kmnhan/erlabpy/commit/53b368813f570cef2c84a9517c618428310a4a2e))

- **utils.array:** add `broadcast_args` decorator for DataArray broadcasting ([76149b9](https://github.com/kmnhan/erlabpy/commit/76149b97c1c380b0f67482d668359715b86251b2))

  Adds a new decorator that enables passing DataArrays to functions that only accepts numpy arrays or always returns numpy arrays, like numba-accelerated functions and some scipy functions.

- **analysis.transform:** add `symmetrize` (#97) ([aefb966](https://github.com/kmnhan/erlabpy/commit/aefb966db44f940a795857b56e6f5d550f53549c))

  Adds a new method `erlab.analysis.transform.symmetrize` for symmetrizing data across a single coordinate.

### 🐞 Bug Fixes

- **imagetool:** center rotation guidelines on cursor position upon initialization ([18a7114](https://github.com/kmnhan/erlabpy/commit/18a711447523b21158f397d5d983d1a4ba8383e5))

- **io.plugins.kriss:** support tilt compensated angle maps ([0229ea2](https://github.com/kmnhan/erlabpy/commit/0229ea21311a187f744543cdf18907f3359ded1d))

- **io:** enforce native endianness for Igor Pro waves (#114) ([92fe389](https://github.com/kmnhan/erlabpy/commit/92fe3899cd655a3919439456f25f4e2e21369456))

  Data loaded from Igor Pro waves will now be converted to have native endianness. Some old data were loaded in big-endian by default, causing incompatibility with several numba functions, with ambiguous error messages.

- **io.plugins.kriss:** properly assign rotation axes names ([3dcb2ae](https://github.com/kmnhan/erlabpy/commit/3dcb2ae26b4e641fd05fb9e573f6306d77850726))

- **imagetool.dialogs:** make new windows opened within data transformation dialogs forget file path information ([7a012cd](https://github.com/kmnhan/erlabpy/commit/7a012cd2a21f8f3a3c65c1be0d50f8854aa3817d))

- **imagetool:** properly handle integer coordinates, closes [#94](https://github.com/kmnhan/erlabpy/issues/94) ([5f0cd36](https://github.com/kmnhan/erlabpy/commit/5f0cd36d4b5bae03f6e689eea45557c55cd3ff45))

- **imagetool:** correct 1D data axis padding ([68f59e9](https://github.com/kmnhan/erlabpy/commit/68f59e903cc9822f665c5c790a8296b7142358fb))

- **imagetool:** allow loading data saved with non-default colormap (#102) ([c476be2](https://github.com/kmnhan/erlabpy/commit/c476be2775fb7f0e2a08f4a74346d419e3dc0e05))

- **io.dataloader:** preserve darr name when loading without values ([3310ed6](https://github.com/kmnhan/erlabpy/commit/3310ed61e0ce7fb6f5569a455252fec5d173e54b))

- **imagetool:** allow data with constant coordinates ([6ed4f2b](https://github.com/kmnhan/erlabpy/commit/6ed4f2b34c6c027cc06c565afa191dd97aa753b4))

- **imagetool.manager:** disable scrolling in image preview ([bd77e8d](https://github.com/kmnhan/erlabpy/commit/bd77e8d17db4a5b09cdacb1263d66da6f2bb8ec5))

- **io.plugins.da30:** zero DA offset for non-DA lens modes (#96) ([a3bdf84](https://github.com/kmnhan/erlabpy/commit/a3bdf8400278a1df9b38d40d7d9a33135bfb0961))

### ♻️ Code Refactor

- move fitting accessors to `xarray-lmfit` (#110) ([9106cef](https://github.com/kmnhan/erlabpy/commit/9106cef37a9c4e1b40ff78fea96ae2b8efd3ce07))

  `DataArray.modelfit` and `Dataset.modelfit` are deprecated. The functionality has been moved to the [xarray-lmfit](https://github.com/kmnhan/xarray-lmfit) package, and can be accessed via `DataArray.xlm.modelfit` and `Dataset.xlm.modelfit` as a drop-in replacement.

- **ktool:** adjust default lattice parameter spinbox step to 0.1 for finer adjustments ([d7cba80](https://github.com/kmnhan/erlabpy/commit/d7cba80eaba9111180d4f05e089931106b83650b))

- improve error message for missing hvplot package ([a0c2460](https://github.com/kmnhan/erlabpy/commit/a0c246024f990f2862915517175a3a4e365c9b22))

- **utils.array:** simplify decorators for 2D array checks ([7275e2e](https://github.com/kmnhan/erlabpy/commit/7275e2e0b276a401f377fb68df195891e61cac0e))

[main 8902951] bump: version 3.7.0 → 3.8.0
 2 files changed, 2 insertions(+), 2 deletions(-)

