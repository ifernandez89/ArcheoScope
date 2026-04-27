# Contributing to Archeoscope

Thank you for your interest in contributing to **Archeoscope: The Forgotten Relics**.

## License Agreement

By contributing to this project, you agree that your contributions will be
licensed under the same **CC BY-NC 4.0** license as the project source code.

You retain copyright of your contributions, but grant Ignacio Fernandez a
perpetual, worldwide, non-exclusive license to use, modify, and distribute
your contributions as part of this project, including in commercial versions.

## What You Can Contribute

- Bug fixes
- Performance improvements
- New archaeological site data (coordinates, descriptions)
- Astronomical data corrections
- Translations and localization
- Documentation improvements
- Accessibility improvements

## What Requires Prior Discussion

- New gameplay features
- Changes to the core engine architecture
- New 3D assets or visual content
- Audio or music additions

## How to Contribute

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-improvement`
3. Make your changes
4. Ensure the build passes: `cd viewer3d && bun run build`
5. Submit a Pull Request with a clear description

## Code Style

- TypeScript strict mode
- React functional components with hooks
- Three.js best practices (dispose geometries/materials, avoid allocations in useFrame)
- Mobile-first performance considerations

## Attribution

All contributors will be credited in the NOTICE file.

## Commercial Use

This project is open for research and educational use under CC BY-NC 4.0.
Commercial licenses are available upon request: nacho.xiphos@gmail.com
