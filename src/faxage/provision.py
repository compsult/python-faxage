from faxage import APIClient, handle_error

PROVISION_URL = '/new_provision.php'

class NPANXXResult(object):
    def __init__(self, region, state):
        self.region = region
        self.state = state

class ProvisioningClient(APIClient):
    def __init__(self, company, username, password):
        super(FaxClient, self).__init__(PROVISION_URL, company, username, password)

    def list_area_codes(self):
        resp = self.send_post('listac')
        handle_error(resp)
        return resp.splitlines()

    def list_npa_nxx(self, area_code=None):
        results = []
        arguments = {}
        if area_code:
            arguments['ac'] = area_code
        resp = self.send_post('listnpanxx', arguments)
        handle_error(resp)
        for line in resp.splitlines():
            # rc, rcstate
            record = line.split('\t')
            results.append(
                NPANXXStatus(
                    record[0],
                    record[1],
                )
            )
        return results

    def list_dids(self, area_code=None, npa_nxx=None):
        if area_code:
            arguments['ac'] = area_code
        if npa_nxx:
            arguments['npanxx'] = npa_nxx
        resp = self.send_post('listdids', arguments)
        return resp.splitlines()

    def allocate(self, *dids):
        for did in dids:
            resp = self.send_post('provdid', {
                'didnumber':                did
            })
            handle_error(resp)

    def release(self, dids):
        for did in dids:
            resp = self.send_post('unprovdid', {
                'didnumber':                did
            })
            handle_error(resp)