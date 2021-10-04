import imagematrix
import time


class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self, dp=True):
        start = time.time()
        #Create dictionary for energy entries
        self.energies = {}
        for i in range(self.width):
            for j in range(self.height):
                #create energy table
                self.energies[i,j] = self.energy(i,j)
        if dp:
            #if DP, do this
            end = time.time()
            timing = end - start
            print(timing)
            return self.best_seam_dp(self.energies)
        else:
            #if recursive, do this
            return self.best_seam_naive(self.energies)
        

    def best_seam_dp(self, energies):
        self.temp = {}
        self.memo = {}
        #Create temp dictionaries
        for i in range(self.width):
            self.memo[i,0] = self.energies[i,0]
            self.temp[i,0] = [(i,0)]

        last_row_min = []
        #Make a list to take the last row minimum for induction steps
        for j in range(1, self.height):
            #Iterate through the height
            for i in range(self.width):
                min_list = []
                min_list_path = {}
                
                #This is just the recurrence formula
                left = (i-1, j-1)
                middle = (i, j-1)
                right = (i+1, j-1)
                if(i == 0):
                    #Checking where we are in DP table
                    options_above = [middle, right]
                elif(i == self.width-1):
                    #If we are on edge
                    options_above = [left, middle]
                else:
                    #We are on middle
                    options_above = [left, middle, right]

                for option in options_above:
                    #Append the values to the min list
                    min_list.append(self.memo[option])
                    min_list_path[self.memo[option]] = option
                
                min_energy = min(min_list)
                #Begin back tracking
                self.memo[i,j] = min_energy + self.energies[i,j]
                
                for m in min_list:
                    if(m == min_energy):
                        self.temp[i,j] = self.temp[min_list_path[m]] + [(i,j)]
                if(j==self.height-1):
                    if(i==0):
                        last_row_min.append(self.memo[i,j])
                        last_row_min.append((i,j))
                        last_row_min.append(min(min_list))
                        last_row_min.append(min_list_path[self.memo[option]])
                    else:
                        if(last_row_min[0]>self.memo[i,j]):
                            last_row_min[0] = self.memo[i,j]                        
                            last_row_min[1] = (i,j)                                 
                            last_row_min[2] = min(min_list)                     
                            last_row_min[3] = min_list_path[self.memo[option]]
                        #Return temp
        return self.temp[last_row_min[3]] + [last_row_min[1]]
  


    def best_seam_naive(self, energies):
        seam = []
        for i in range(self.width-1):
            seam = self.recursive_best_seam(i,0)
        return seam

    def recursive_best_seam(self, i, j):
        if(j == self.height-1):
            return [(i,j)]
        else:
            if(i == 0):
                # no left
                middle = self.recursive_best_seam(i, j+1)
                right = self.recursive_best_seam(i+1, j+1)
                seams = [middle, right]
                seam_energies = [self.seam_energy(middle), \
                                self.seam_energy(right)]

            elif(i == self.width-1):
                left = self.recursive_best_seam(i-1, j+1)
                middle = self.recursive_best_seam(i, j+1)
                # no right
                seams = [left, middle]
                seam_energies = [self.seam_energy(left), \
                                self.seam_energy(middle)]
            else:
                left = self.recursive_best_seam(i-1, j+1)
                middle = self.recursive_best_seam(i, j+1)
                right = self.recursive_best_seam(i+1, j+1)
                seams = [left, middle, right]
                seam_energies = [self.seam_energy(left), \
                                self.seam_energy(middle), \
                                self.seam_energy(right)]

            best_seam_index = seam_energies.index(min(seam_energies))
            best_seam_here = seams[best_seam_index]

            return [(i,j)] + best_seam_here


    def seam_energy(self, seam):
        sum = 0
        for s in seam:
            sum += self.energies[s]
        return sum
    
import timeit
