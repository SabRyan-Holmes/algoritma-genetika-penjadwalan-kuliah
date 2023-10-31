from PyQt5 import QtCore, QtWidgets
from components import Database as db, ResourceTracker, ScheduleParser, ScenarioComposer, AlgoritmaGenetika
from py_ui import Generate as Parent
# from py_ui import Hasil
from sqlite3 import Binary
from numpy import mean
import pickle
import copy


class Generate:
    def __init__(self):
        self.totalResource = {
            'cpu': [],
            'memory': []
        }
        self.tick = 0
        self.data = {
            'results': [],
            'rooms': [],
            'instructors': [],
            'subjects': [],
            # 'sections': [],
            # 'sharings': [],
        }
        self.topChromosomes = []
        self.meta = []
        self.preview = True
        self.sectionKeys = []
        # Mendapatkan data dari Scenario Composer
        composer = ScenarioComposer.ScenarioComposer()
        composer = composer.getScenarioData()
        # update dan masukkan ke data
        self.data.update(composer)
        self.dialog = dialog = QtWidgets.QDialog(parent=None)
        # Initialize custom dialog
        self.parent = parent = Parent.Ui_Dialog()
        # Add parent to custom dialog
        parent.setupUi(dialog)
        dialog.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint)
        self.time = QtCore.QTime(0, 0)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(1000)
        self.running = True
        self.table = parent.tableSchedule
        parent.btnPause.clicked.connect(self.togglePause)
        parent.btnStop.clicked.connect(self.stopOperation)
        parent.chkPreview.clicked.connect(self.togglePreview)
        parent.cmbSection.clear()
        # for section, details in self.data['sections'].items():
        #     self.sectionKeys.append(section)
        #     parent.cmbSection.addItem(details[0])
        parent.cmbSection.currentIndexChanged.connect(self.changePreview)
        self.startWorkers()
        dialog.exec_()

    def togglePreview(self, state):
        self.preview = not state

    def togglePause(self):
        self.toggleState()
        self.parent.btnPause.setText('Pause Generation' if self.running else 'Resume Generation')

    def toggleState(self, state=None):
        self.running = (not self.running) if state is None else state
        self.resourceWorker.running = self.running
        # Ini nanti diubah
        self.AlgoritmaGenetika.running = self.running

    def startWorkers(self):
        self.resourceWorker = ResourceTrackerWorker()
        self.resourceWorker.signal.connect(self.updateResource)
        self.resourceWorker.start()
        self.AlgoritmaGenetika = AlgoritmaGenetika.AlgoritmaGenetika(self.data)
        self.AlgoritmaGenetika.statusSignal.connect(self.updateStatus)
        self.AlgoritmaGenetika.detailsSignal.connect(self.updateDetails)
        self.AlgoritmaGenetika.dataSignal.connect(self.updateView)
        self.AlgoritmaGenetika.operationSignal.connect(self.updateOperation)
        Hasil = self.AlgoritmaGenetika.results 
        Solusi = self.AlgoritmaGenetika.getJumlahSolusi() 
        
        
        self.AlgoritmaGenetika.start()

    def updateStatus(self, status):
        self.parent.lblStatus.setText('Status: {}'.format(status))

    def updateDetails(self, details):
        # details = {
        
        #     'Generasi' : self.AlgoritmaGenetika.generation,
        #     'AvgFitness' : self.AlgoritmaGenetika.AverageFitness,
        #     'Past_Avg_fitness' : self.AlgoritmaGenetika.pastAverageFitness,
        #     'HighestFitness' : self.AlgoritmaGenetika.highestFitness,
        #     'LowestFitness': self.AlgoritmaGenetika.lowestFitnessFitness,
        # }
        # Generasi = details['Generasi'],
        # Avg_fitness = details['Avg_fitness'],
        # Past_Avg_fitness = details['Past_Avg_fitness'],
        # HighestFitness = details['HighestFitness'],
        # LowestFitness = details['LowestFitness'],

        # format(details)
        self.parent.boxGen.setTitle('Generation #')
        self.parent.lblPopulation.setText('Population: ' )
        self.parent.lblMutation.setText('Mutation Rate:')
        self.parent.lblFitness.setText('Average Fitness: ')
        self.parent.lblPreviousFitness.setText('Previous Average Fitness: ')
        self.parent.lblHighestFitness.setText('Highest Fitness: ')
        self.parent.lblLowestFitness.setText('Lowest Fitness:')
        
        # self.parent.boxGen.setTitle('Generation #{}'.format(details[0]))
        # self.parent.lblPopulation.setText('Population: {}'.format(details[1]))
        # self.parent.lblMutation.setText('Mutation Rate: 50%'.format(details[2]))
        # self.parent.lblFitness.setText('Average Fitness: {}%'.format(details[3]))
        # self.parent.lblPreviousFitness.setText('Previous Average Fitness: {}%'.format(details[4]))
        # self.parent.lblHighestFitness.setText('Highest Fitness: {}%'.format(details[5]))
        # self.parent.lblLowestFitness.setText('Lowest Fitness: {}%'.format(details[6]))

    def updateView(self, chromosomes):
        chromosomes.reverse()
        self.topChromosomes = copy.deepcopy(chromosomes)
        self.changePreview(self.parent.cmbSection.currentIndex())

    def changePreview(self, index):
        data = []
        if not len(self.topChromosomes) or not self.preview:
            return False
        # sections = self.topChromosomes[0][0].data['sections']
        rawData = self.data
        # subjects = sections[self.sectionKeys[index]]['details']
        # for subject, details in subjects.items():
        #     if not len(details):
        #         continue
        #     instructor = '' if not details[1] else rawData['instructors'][details[1]][0]
        #     data.append({'color': None, 'text': '{} \n {} \n {}'.format(rawData['subjects'][subject][0],
        #                                                                 rawData['rooms'][details[0]][0],
        #                                                                 instructor),
        #                  'instances': [[day, details[3], details[3] + details[4]] for day in details[2]]})
        # self.loadTable(data)

    # def loadTable(self, results=[], solusi):
    #     Hasil.Hasil(results, solusi)
        # self.table.reset()
        # self.table.clearSpans()
        # ScheduleParser.ScheduleParser(self.table, data)

    def updateOperation(self, type):
        if type == 1:
            self.stopOperation()


    def updateTime(self):
        self.time = self.time.addSecs(1)
        self.parent.lblTime.setText('Elapsed Time: {}'.format(self.time.toString('hh:mm:ss')))

    def stopOperation(self):
        self.toggleState(False)
        self.resourceWorker.terminate()
        self.resourceWorker.runThread = False
        # self.genericAlgorithm.terminate()
        self.AlgoritmaGenetika.terminate()
        self.timer.stop()
        if len(self.topChromosomes):
            self.parent.btnStop.setText('View Result')
            self.parent.btnStop.clicked.disconnect(self.stopOperation)
            self.parent.btnStop.clicked.connect(self.dialog.close)
            self.parent.lblCPU.setText('CPU Usage: Stopped')
            self.parent.lblMemory.setText('Memory Usage: Stopped')
            self.parent.lblStatus.setText('Status: Stopped')
            self.totalResource['cpu'] = mean(self.totalResource['cpu'])
            self.totalResource['memory'] = mean(self.totalResource['memory'])
            self.meta = [[chromosome[1], chromosome[0].fitnessDetails] for chromosome in
                         self.topChromosomes]
            conn = db.getConnection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO results (content) VALUES (?)', [Binary(
                pickle.dumps({'data': [chromosome[0].data for chromosome in self.topChromosomes],
                              'meta': self.meta,
                              'time': self.time.toString('hh:mm:ss'),
                              'resource': self.totalResource,
                              'rawData': self.data},
                             pickle.HIGHEST_PROTOCOL))])
            conn.commit()
            conn.close()
        else:
            self.dialog.close()

    def updateResource(self, resource):
        self.tick += 1
        if self.tick == 3:
            self.tick = 0
        else:
            self.totalResource['cpu'].append(resource[0])
            self.totalResource['memory'].append(resource[1][1])
        self.parent.lblCPU.setText('CPU Usage: {}%'.format(resource[0]))
        self.parent.lblMemory.setText('Memory Usage: {}% - {} MB'.format(resource[1][0], resource[1][1]))


class ResourceTrackerWorker(QtCore.QThread):
    signal = QtCore.pyqtSignal(object)
    running = True
    runThread = True

    def __init__(self):
        super().__init__()

    def __del__(self):
        self.wait()

    def run(self):
        while (self.runThread):
            self.sleep(1)
            if self.running is True:
                cpu = ResourceTracker.getCPUUsage()
                memory = ResourceTracker.getMemoryUsage()
                memory = [ResourceTracker.getMemoryPercentage(memory), ResourceTracker.byteToMegabyte(memory[0])]
                self.signal.emit([cpu, memory])
        return True
