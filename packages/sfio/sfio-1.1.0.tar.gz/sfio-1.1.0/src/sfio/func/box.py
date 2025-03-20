__all__ = []

import numpy as np

from .. import logger
from . import flatten


class BoxFunc:
    def fractional_xyz(self, pts: np.ndarray) -> np.ndarray:
        pts = np.atleast_2d(pts)
        _ = self.output
        lo = np.array([_['xlo'], _['ylo'], _['zlo']])
        norm = np.sum(np.dot(_['v'], _['bn'].T) ** 2.0, axis=1) ** 0.5
        return np.dot(pts - lo, _['bn'].T) / norm

    def bounding_box_check(self, pts: np.ndarray) -> dict:
        """check which points in pts is within bounding box"""
        # TODO: pbc on selected faces
        # pbc = list(flatten([pbc])*3)[:3]  # direction a, b, c

        _ = self.output
        pts = np.atleast_2d(pts)

        # lo and hi of each point
        lo = np.array([_['xlo'], _['ylo'], _['zlo']]) - pts
        hi = lo + np.sum(_['v'], axis=0)

        # normal vectors of box faces
        bn = _['bn']

        # distance from origin to box faces
        # (face_xlo face_ylo face_zlo face_xhi face_yhi face_zhi)
        dist = np.c_[
            np.dot(-bn, np.atleast_2d(lo).T).T,
            np.dot(bn, np.atleast_2d(hi).T).T,
        ]
        inside = np.min(dist, axis=1) >= 0
        N = pts.shape[0] - np.sum(inside)

        if N > 0:
            ix_outbound = np.where(~inside)[0]
            logger.debug(
                f"{N} points outside of bounding box, 0-index:\n{ix_outbound}"
            )

        return {
            'inbound': inside,
            'outbound': ~inside,
            'dist': dist,
        }

    def extend(self, pts: np.ndarray, bbcheck=None, pbc=False):
        """extend bounding box to accommodate pts, modify in-place"""

        _ = self.output
        pts = np.atleast_2d(pts)

        if bbcheck is None:
            bbcheck = self.bounding_box_check(pts)
        if np.sum(bbcheck['ix_in']) == pts.shape[0]:
            return self
        pbc = (list(flatten(pbc)) * 3)[:3]  # direction a, b, c
        lo0 = np.array([_['xlo'], _['ylo'], _['zlo']])
        # edit lo end
        lo1 = (_['xlo'], _['ylo'], _['zlo']) = np.min(
            np.r_[pts[bbcheck['ix_out']] - 1e-7, np.atleast_2d(lo0)], axis=0
        ) * (~np.array(pbc)).astype(int)
        shift = np.dot(_['u'], np.atleast_2d(lo1 - lo0).T).T
        # edit hi end
        d = pts[bbcheck['ix_out']] - lo0
        d_abc = np.dot(_['u'], np.atleast_2d(d).T).T
        _['v'] = _['u'] * (
            np.atleast_2d(
                np.maximum(
                    (np.max(d_abc, axis=0) + 1e-7)
                    * (~np.array(pbc)).astype(int),
                    np.sum(_['v'] ** 2.0, axis=1) ** 0.5,
                )
            ).T
            - shift.T
        )
        self.set_input(_['v'], 'basis')  # extend box
        return self

    def wrap(self, pts: np.ndarray, bbcheck=None, pbc=True):
        """move pts to wrap them within bounding box"""

        _ = self.output
        pts = np.atleast_2d(pts)

        if bbcheck is None:
            bbcheck = self.bbcheck(pts)
        if np.sum(bbcheck['ix_in']) == pts.shape[0]:
            return pts

        pbc = (list(flatten(pbc)) * 3)[:3]  # direction a, b, c
        rep = np.abs(
            np.floor_divide(
                bbcheck['dist'],
                np.tile(np.sum(_['v'] ** 2.0, axis=1) ** 0.5, 2),
            )
            * np.tile(pbc, 2).astype(int)
        )
        rep[bbcheck['dist'] >= 0] = 0
        shift = np.sum(
            np.multiply(
                np.ravel(rep).reshape(-1, 1),
                np.tile(np.r_[_['v'], -_['v']], (pts.shape[0], 1)),
            ).reshape(-1, 6, 3),
            axis=1,
        )
        return pts + shift

    def ghost(self, pts: np.ndarray, pbc=True):
        """get ghost pts in periodic images.

        Must wrap out-of-bound atoms first
        i.e.,  pts = box.wrap(pts)
               for pt in box.ghost(pts):
                   ....
        """

        _ = self.output
        pts = np.atleast_2d(pts)

        pbc = (list(flatten(pbc)) * 3)[:3]  # direction a, b, c
        ref = pts  # np.copy(pts)
        L = np.array([_['a'] * pbc[0], _['b'] * pbc[1], _['c'] * pbc[2]])
        shift = L[0] * _['u'][0] + L[1] * _['u'][1] + L[2] * _['u'][2]
        side = (
            np.argmin(
                np.c_[
                    np.sum((pts - shift) ** 2.0, axis=1),
                    np.sum((pts + shift) ** 2.0, axis=1),
                ],
                axis=1,
            )
            * 2
            - 1
        )
        yield ref + np.outer(side, shift)
        for i in (0, 1, 2):
            shift = L[i] * _['u'][i]
            yield ref + np.outer(side, shift)
        for i, j in zip((0, 1, 2), (1, 2, 0)):
            shift = L[i] * _['u'][i] + L[j] * _['u'][j]
            yield ref + np.outer(side, shift)
