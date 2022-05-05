import clusters
import sys

docs,words,data=clusters.readfile(sys.argv[1])

clust=clusters.hcluster(data,distance=clusters.pearson)
print ('clusters by pearson correlation')
clusters.printclust(clust,labels=docs)
clusters.drawdendrogram(clust,docs,jpeg='docsclustpearson.jpg')

clust=clusters.hcluster(data,distance=clusters.tanimoto)
print ('clusters by tanimoto coefficient')
clusters.printclust(clust,labels=docs)
clusters.drawdendrogram(clust,docs,jpeg='docsclusttanimoto.jpg')

clust=clusters.hcluster(data,distance=clusters.euclidean)
print ('clusters by euclidean distance')
clusters.printclust(clust,labels=docs)
clusters.drawdendrogram(clust,docs,jpeg='docsclusteuclidean.jpg')
