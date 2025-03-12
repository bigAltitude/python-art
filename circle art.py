# -*- coding: utf-8 -*-
# Circle Fitting with Blue Shades and Randomization
# Date: 2025-03-08
# Author: S Perkins
# Company: Geo Consulting Limited
# Work: Geo-Science Engineering

import numpy as np
import time
from PIL import Image

FIELD_SIZE = 7500
MAX_R      = 200
STOP_FREE_PERCENT = 5  # Stop when free pixels are below 2% of total
LOG_INT    = 100
THUMB_INT  = 1000

# Base blue intensity: 35% of 255 ≈ 89
BASE_INT   = 55
# Intensity range from 35% to 100% blue:
INT_RANGE  = 200  # (255 - 89)

def get_rand_free(fmask, free_count):
    tot = fmask.size
    if free_count/tot < 0.05:
        inds = np.flatnonzero(fmask)
        idx  = np.random.choice(inds)
        return np.unravel_index(idx, fmask.shape)
    while True:
        idx = np.random.randint(0, tot)
        if fmask.flat[idx]:
            return np.unravel_index(idx, fmask.shape)

def disk_free(i, j, r, fmask):
    h, w = fmask.shape
    if i - r < 0 or i + r >= h or j - r < 0 or j + r >= w:
        return False
    y, x = np.ogrid[-r:r+1, -r:r+1]
    mask = x*x + y*y <= r*r
    sub  = fmask[i-r:i+r+1, j-r:j+r+1]
    return np.all(sub[mask])

def max_free_radius(i, j, fmask):
    h, w = fmask.shape
    rb = min(i, j, h-1-i, w-1-j)
    rmax = min(MAX_R, rb)
    lo, hi = 0, rmax
    while lo < hi:
        mid = (lo+hi+1)//2
        if disk_free(i, j, mid, fmask):
            lo = mid
        else:
            hi = mid-1
    return lo

def fill_disk(i, j, r, field, fmask, shade):
    y, x = np.ogrid[-r:r+1, -r:r+1]
    mask = x*x + y*y <= r*r
    field[i-r:i+r+1, j-r:j+r+1, 2][mask] = shade
    fmask[i-r:i+r+1, j-r:j+r+1][mask] = False
    return np.count_nonzero(mask)

def show_thumb(field, it):
    thumb = field[::20, ::20]
    im = Image.fromarray(thumb, 'RGB')
    im.save(f"thumb_{it}.tiff")

def expand_and_move(i, j, fmask, circles):
    tol = 2
    r = max_free_radius(i, j, fmask)
    improved = True
    while improved and r < MAX_R:
        improved = False
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                ni, nj = i+di, j+dj
                if (ni < 0 or ni >= fmask.shape[0] or
                    nj < 0 or nj >= fmask.shape[1]):
                    continue
                if not fmask[ni, nj]:
                    continue
                nr = max_free_radius(ni, nj, fmask)
                if nr > r:
                    i, j, r = ni, nj, nr
                    improved = True
                    break
            if improved:
                break
    while r < MAX_R:
        if disk_free(i, j, r+1, fmask):
            r += 1
            moved = False
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if di == 0 and dj == 0:
                        continue
                    ni, nj = i+di, j+dj
                    if (ni < 0 or ni >= fmask.shape[0] or
                        nj < 0 or nj >= fmask.shape[1]):
                        continue
                    if not fmask[ni, nj]:
                        continue
                    nr = max_free_radius(ni, nj, fmask)
                    if nr > r:
                        i, j, r = ni, nj, nr
                        moved = True
                        break
                if moved:
                    break
            if len(circles) >= 3:
                count = 0
                for (ci, cj, cr) in circles:
                    d = np.sqrt((i-ci)**2+(j-cj)**2)
                    if abs(d - (r+cr)) < tol:
                        count += 1
                    if count >= 3:
                        return i, j, r
        else:
            break
    return i, j, r

def main():
    start = time.time()
    # Create a 3-channel RGB image, all pixels black.
    field = np.zeros((FIELD_SIZE, FIELD_SIZE, 3), dtype=np.uint8)
    fmask = np.ones((FIELD_SIZE, FIELD_SIZE), bool)
    free_count = fmask.sum()
    circles = []  # list of (i, j, r)
    iter_count = 0

    total_pixels = fmask.size
    stop_threshold = total_pixels * (STOP_FREE_PERCENT / 100.0)

    # Place first circle
    i, j = get_rand_free(fmask, free_count)
    i, j, r = expand_and_move(i, j, fmask, circles)
    # If fully free, assign a random radius between 20 and MAX_R.
    if r == MAX_R:
        r = np.random.randint(20, MAX_R+1)
    shade = int((r/MAX_R) * INT_RANGE + BASE_INT)
    num = fill_disk(i, j, r, field, fmask, shade)
    free_count -= num
    circles.append((i, j, r))
    iter_count += 1
    if iter_count % LOG_INT == 0:
        print(f"Iter {iter_count}, free: {free_count}")
    while free_count > stop_threshold:
        i, j = get_rand_free(fmask, free_count)
        i, j, r = expand_and_move(i, j, fmask, circles)
        if r == MAX_R:
            r = np.random.randint(20, MAX_R+1)
        shade = int((r/MAX_R) * INT_RANGE + BASE_INT)
        num = fill_disk(i, j, r, field, fmask, shade)
        free_count -= num
        circles.append((i, j, r))
        iter_count += 1
        if iter_count % LOG_INT == 0:
            print(f"Iter {iter_count}, free: {free_count}")
        if iter_count % THUMB_INT == 0:
            show_thumb(field, iter_count)
    im = Image.fromarray(field, 'RGB')
    im.save("circle_field_blue_random.tiff")
    end = time.time()
    print(f"Done in {end-start:.1f}s, iter: {iter_count}")

if __name__=='__main__':
    main()
