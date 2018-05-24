# -*- coding: utf-8 -*-
from chapter3.generatefeedvector import genetatefeedvector
import chapter3.clusters as clusters


def test_generatefeedvector():
    genetatefeedvector('data/feedlist.txt', 'output/blogdata.txt', 'Blog')


def test_print_hierarchical_cluster():
    blognames, words, data = clusters.readfile('data/blogdata.txt')
    cluster = clusters.hcluster(data)
    clusters.printhcluster(cluster, labels=blognames)


def test_print_column_hierarchical_cluster():
    blognames, words, data = clusters.readfile('data/blogdata.txt')
    cluster = clusters.hcluster(clusters.rotatematrix(data))
    clusters.printhcluster(cluster, labels=words)


def test_k_mean_cluster():
    blognames, words, data = clusters.readfile('data/blogdata.txt')
    cluster = clusters.kcluster(data)
    clusters.printkcluster(cluster, labels=blognames)


def test_scale_down():
    blognames, words, data = clusters.readfile('data/blogdata.txt')
    cluster = clusters.scaledown(data)
    print cluster


if __name__ == "__main__":
    test_scale_down()
