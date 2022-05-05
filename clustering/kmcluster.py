import clusters
import sys

docs,words,data=clusters.readfile(sys.argv[1])


print ('2 clusters:')
clust=clusters.kcluster(data,distance=clusters.pearson,k=sys.argv[2])
print ('clusters by pearson correlation')
for i in range(len(clust)):
    print('cluster '+ str(i) + ':\n' + str([docs[r] for r in clust[i]]))


# clust=clusters.kcluster(data,distance=clusters.tanimoto,k=2)
# print ('clusters by tanimoto coefficient')
# print ('cluster 1:')
# print ([docs[r] for r in clust[0]])
# print ('cluster 2:')
# print ([docs[r] for r in clust[1]])
#
# clust=clusters.kcluster(data,distance=clusters.euclidean,k=2)
# print ('clusters by euclidean distance')
# print ('cluster 1:')
# print ([docs[r] for r in clust[0]])
# print ('cluster 2:')
# print ([docs[r] for r in clust[1]])
